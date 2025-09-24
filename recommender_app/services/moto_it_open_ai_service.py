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
from recommender_app.schemas.version_query_result import VersionQueryResult
from typing import Any

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

    def ask(self, message: str, session_id: int | None = None) -> dict:
        if not session_id:
            # TODO: recuperare l'ID reale dell'utente autenticato quando disponibile
            user_id = 1
            session_id = self.session_service.create_session(user_id=user_id)

        self.session_service.append_message(session_id, message, sender="user")

        sql_query = None
        rows: list[dict] = []

        try:
            retrievals = self.query_engine.retrieve(message)
            if retrievals:
                sql_query = retrievals[0].raw_query
                logging.debug(f"Generated SQL Query: {sql_query}")
        except Exception as exc:
            logging.error(f"SQL retrieval error: {exc}")

        if sql_query:
            rows = self._execute_sql_query(sql_query)

        answer = ""
        try:
            response = self.query_engine.query(message)
            answer = str(response)
        except Exception as exc:
            logging.error(f"Response generation error: {exc}")
            return {
                'session_id': session_id,
                'sql_query': sql_query,
                'rows': rows,
                'answer': answer,
                'error': str(exc)
            }

        self.session_service.append_message(session_id, answer, sender="bot")

        return {
            'session_id': session_id,
            'sql_query': sql_query,
            'rows': rows,
            'answer': answer
        }

    def _execute_sql_query(self, sql_query: str) -> list[dict]:
        structured_rows: list[dict] = []
        try:
            result = self.sql_database.run_sql(sql_query)
            for row in result:
                row_dict = self._row_to_dict(row)
                structured_rows.append(self._structure_row(row_dict))
        except Exception as exc:
            logging.error(f"SQL execution error: {exc}")
        return structured_rows

    @staticmethod
    def _row_to_dict(row: Any) -> dict:
        if hasattr(row, '_mapping'):
            return dict(row._mapping)
        if isinstance(row, dict):
            return dict(row)
        try:
            return dict(row)
        except (TypeError, ValueError):
            return {'value': row}

    @staticmethod
    def _structure_row(row_dict: dict) -> dict:
        lower_map = {k.lower(): v for k, v in row_dict.items() if isinstance(k, str)}
        data = {'raw': row_dict}
        for field_name in VersionQueryResult.model_fields:
            if field_name == 'raw':
                continue
            if field_name in row_dict:
                data[field_name] = row_dict[field_name]
            elif field_name in lower_map:
                data[field_name] = lower_map[field_name]
        return VersionQueryResult(**data).model_dump()

