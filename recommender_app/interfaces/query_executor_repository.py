from typing import Protocol


class QueryExecutorRepository(Protocol):
    """Repository per l'esecuzione di query SQL dinamiche."""
    
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
        pass
