"""DEPRECATO - Usare openai-agents invece."""
import logging
from recommender_app.agents.sql_rag_gate_agent import sql_rag_gate_agent_runner
from recommender_app.agents.sql_query_generator_agent import sql_query_generator_agent_runner, refresh_sql_query_generator_agent_categories
from recommender_app.agents.simple_motorcycle_chat_agent import simple_motorcycle_chat_agent_runner
from recommender_app.services.category_service import CategoryService
from recommender_app.services.query_executor_service import QueryExecutorService
from recommender_app.services.ranking_service import deduplicate_versions



class MotoItOpenAiBotService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.categorySvc = CategoryService()
        self.queryExecutorSvc = QueryExecutorService()
    
    async def ask(self, message: str, session_id: int | None = None) -> dict:
        result = await sql_rag_gate_agent_runner(message)
        
        if result.is_sql_query:
            self.logger.info(f"Session {session_id}: SQL query needed. Reasoning: {result.reasoning}")
            categories_tuples = self.categorySvc.list_categories_as_tuples()
            refresh_sql_query_generator_agent_categories(categories_tuples)            
            sql = await sql_query_generator_agent_runner(message)
            
            # Esegui la query SQL e ottieni i risultati grezzi
            rows = self.sql_executor(sql.sql_query)
            total_raw = len(rows)
            dedup_rows = deduplicate_versions(rows, limit=20)
            message = f"Ho eseguito una query sul database: {total_raw} risultati grezzi, mostrati {len(dedup_rows)} modelli (deduplicati per modello)."

            return {
                "answer": message,
                "reasoning": result.reasoning,
                "rows": dedup_rows,
                "session_id": session_id,
                "sql_query": sql.sql_query,
                "total_raw_results": total_raw
            }
            
        else:
            self.logger.info(f"Session {session_id}: No SQL query needed. Reasoning: {result.reasoning}")
            chat_response = await simple_motorcycle_chat_agent_runner(message)
            message = chat_response.answer
        
        return {
            "answer": message,
            "reasoning": result.reasoning,
            "rows": [],
            "session_id": session_id,
            "sql_query": None
        }
        
        
        
    def sql_executor(self, sql_query: str) -> list[dict]:
        """
        Esegue una query SQL e restituisce i risultati.
        
        Args:
            sql_query: Query SQL da eseguire
            
        Returns:
            Lista di dizionari contenenti i risultati della query
        """
        try:
            return self.queryExecutorSvc.execute_query(sql_query)
        except Exception as e:
            self.logger.error(f"Errore nell'esecuzione della query SQL: {str(e)}")
            return []



