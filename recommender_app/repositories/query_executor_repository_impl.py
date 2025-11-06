import logging
from typing import Any
from sqlalchemy import text
from sqlalchemy.orm import Session
from recommender_app.interfaces.query_executor_repository import QueryExecutorRepository


class QueryExecutorRepositoryImpl(QueryExecutorRepository):
    """Implementazione del repository per l'esecuzione di query SQL dinamiche."""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.logger = logging.getLogger(__name__)
    
    def execute_raw_query(self, sql_query: str) -> list[dict]:
        """
        Esegue una query SQL raw e restituisce i risultati come lista di dizionari.
        
        Args:
            sql_query: Query SQL da eseguire (solo SELECT supportate per sicurezza)
            
        Returns:
            Lista di dizionari contenenti i risultati della query
            
        Raises:
            ValueError: Se la query non è una SELECT o contiene operazioni non sicure
        """
        # Validazione base: accetta solo SELECT
        normalized_query = sql_query.strip().upper()
        if not normalized_query.startswith('SELECT'):
            raise ValueError("Solo query SELECT sono permesse per motivi di sicurezza")
        
        # Verifica che non ci siano operazioni pericolose
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE', 'EXEC', 'EXECUTE']
        for keyword in dangerous_keywords:
            if keyword in normalized_query:
                raise ValueError(f"Operazione non permessa: {keyword}")
        
        try:
            self.logger.info(f"Esecuzione query SQL: {sql_query}")
            
            # Esegui la query usando text() per query raw
            result = self.db_session.execute(text(sql_query))
            
            # Converti i risultati in lista di dizionari
            rows = []
            for row in result:
                # Ottieni i nomi delle colonne
                row_dict = dict(row._mapping)
                rows.append(row_dict)
            
            self.logger.info(f"Query eseguita con successo. Righe restituite: {len(rows)}")
            return rows
            
        except Exception as e:
            self.logger.error(f"Errore nell'esecuzione della query SQL: {str(e)}")
            raise
