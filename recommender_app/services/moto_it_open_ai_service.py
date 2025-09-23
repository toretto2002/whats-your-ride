import logging
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core import SQLDatabase
from recommender_app.db_ses.session import llama_engine
from llama_index.embeddings.openai import OpenAIEmbedding
from recommender_app.core.config import Config  # dove hai messo la OPENAI_API_KEY
from recommender_app.utils.file_loader import load_prompt
from recommender_app.services.session_service import SessionService

class MotoItOpenAiBotService:
    def __init__(self):
        # Logging
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
        self.logger = logging.getLogger(__name__)
        self.session_service = SessionService()


        # ChatGPT LLM (via llama-index)
        self.llm = LlamaOpenAI(
            api_key=Config.OPENAI_API_KEY,
            model="gpt-4o",  # oppure "gpt-3.5-turbo"
            temperature=0.7
        )

        # Embedding model OpenAI
        Settings.embed_model = OpenAIEmbedding(api_key=Config.OPENAI_API_KEY)

        # SQL DB setup
        self.sql_database = SQLDatabase(
            llama_engine,
            include_tables=["brands", "models", "versions", "categories"],
            sample_rows_in_table_info=2,
            custom_table_info = {
                "versions": load_prompt("utils/prompts/moto_it/custom_table_info.txt")
            }
        )

        # Query engine
        self.query_engine = NLSQLTableQueryEngine(
            sql_database=self.sql_database,
            llm=self.llm,
            system_prompt = load_prompt("utils/prompts/moto_it/system_prompt.txt")
        )

    def ask(self, data, session_id: int | None = None) -> str | dict:
        try:
            query = self.query_engine.retriever.retrieve(data)[0].raw_query
            logging.debug(f"Generated SQL Query: {query}")
        except Exception as e:
            logging.error(f"SQL Error: {e}")

        try:
            
            response = self.query_engine.query(data)

            if not session_id:
                user_id = 1  # Recupera l'ID dell'utente da qualche parte
                session_id = self.session_service.create_session(user_id=user_id)

           
            self.session_service.append_message(session_id, data, sender="user")
            self.session_service.append_message(session_id, str(response), sender="bot")
    
            
            return {"res": str(response), "session_id": session_id}
        except Exception as e:
            logging.error(f"Execution Error: {e}")
            return {"error": str(e)}
