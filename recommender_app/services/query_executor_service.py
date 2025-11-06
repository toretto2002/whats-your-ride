import logging
from recommender_app.extensions import db
from recommender_app.repositories.query_executor_repository_impl import QueryExecutorRepositoryImpl


class QueryExecutorService:
    """Servizio per l'esecuzione di query SQL dinamiche."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.repository = QueryExecutorRepositoryImpl(db.session)
    
    def execute_query(self, sql_query: str) -> list[dict]:
        """
        Esegue una query SQL e restituisce i risultati.
        
        Args:
            sql_query: Query SQL da eseguire
            
        Returns:
            Lista di dizionari con i risultati
        """
        try:
            return self.repository.execute_raw_query(sql_query)
        except Exception as e:
            self.logger.error(f"Errore nel servizio di esecuzione query: {str(e)}")
            raise
