"""
OPZIONALE: Questo servizio usa llama-index con Ollama (modelli locali).
Può essere mantenuto se vuoi supportare modelli locali, oppure migrato a openai-agents.

Migration path (opzionale): OllamaMotorcycleQueryAgent

NOTA: llama-index-llms-ollama e llama-index-embeddings-ollama 
      possono rimanere se vuoi mantenere il supporto Ollama locale.
"""

from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core import SQLDatabase
from recommender_app.db_ses.session import llama_engine
from llama_index.embeddings.ollama import OllamaEmbedding
import logging


class BotService:
    """
    Servizio per modelli Ollama locali.
    
    OPZIONALE: Può essere mantenuto con llama-index o migrato a openai-agents.
    """

    def __init__(self):

        # Configurazione del logging
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
        self.logger = logging.getLogger(__name__)

        
        self.llm = Ollama(model="phi", base_url="http://ollama:11434", request_timeout=120)
        
        Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
        
        self.sql_database = SQLDatabase(
            llama_engine,
            include_tables=["motorcycles"],  # puoi anche rimuovere questo argomento per tutte
            sample_rows_in_table_info=2,
        )

        self.query_engine = NLSQLTableQueryEngine(
            sql_database=self.sql_database,
            llm=self.llm,
        )
            

    
    def ask(self, data):
        try:
            query = self.query_engine.retriever.retrieve(data)[0].raw_query
            logging.debug(f"Generated SQL Query: {query}")
        except Exception as e:
            logging.error(f"SQL Error: {e}")

        try:
            response = self.query_engine.query(data)
            return str(response)
        except Exception as e:
            logging.error(f"Execution Error: {e}")
            return {"error": str(e)}
