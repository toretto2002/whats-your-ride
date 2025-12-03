"""DEPRECATO - Usare openai-agents invece."""
import logging
from recommender_app.agents.sql_rag_gate_agent import sql_rag_gate_agent_runner
from recommender_app.agents.sql_query_generator_agent import sql_query_generator_agent_runner, refresh_sql_query_generator_agent_categories
from recommender_app.agents.simple_motorcycle_chat_agent import simple_motorcycle_chat_agent_runner
from recommender_app.agents.answer_synthesis_agent import answer_synthesis_agent_runner
from recommender_app.agents.comparator_agent import comparator_agent_runner
from recommender_app.services.category_service import CategoryService
from recommender_app.services.query_executor_service import QueryExecutorService
from recommender_app.services.ranking_service import deduplicate_versions



class MotoItOpenAiBotService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.categorySvc = CategoryService()
        self.queryExecutorSvc = QueryExecutorService()
    
    async def ask(self, message: str, session_id: int | None = None, comparison_ids: list[int] | None = None) -> dict:
        original_user_message = message
        result = await sql_rag_gate_agent_runner(original_user_message)
        
        if result.is_sql_query and not comparison_ids:
            self.logger.info(f"Session {session_id}: SQL query needed. Reasoning: {result.reasoning}")
            categories_tuples = self.categorySvc.list_categories_as_tuples()
            refresh_sql_query_generator_agent_categories(categories_tuples)
            sql = await sql_query_generator_agent_runner(original_user_message)

            # Esegui la query SQL e ottieni i risultati grezzi
            rows = self.sql_executor(sql.sql_query)
            total_raw = len(rows)
            dedup_rows = deduplicate_versions(rows, limit=20)

            # Sintesi finale con nuovo agente
            meta = {
                "total_raw_results": total_raw,
                "shown_models": len(dedup_rows),
                "session_id": session_id,
            }
            synthesis = await answer_synthesis_agent_runner(
                user_message=original_user_message,
                items=dedup_rows,
                meta=meta,
            )

            combined_reasoning = f"Gate: {result.reasoning}\nSynthesis: {synthesis.reasoning}" if synthesis.reasoning else result.reasoning

            return {
                "answer": synthesis.answer,
                "reasoning": combined_reasoning,
                "rows": dedup_rows,
                "session_id": session_id,
                "sql_query": sql.sql_query,
                "total_raw_results": total_raw
            }
            
        elif not result.is_sql_query:
            self.logger.info(f"Session {session_id}: No SQL query needed. Reasoning: {result.reasoning}")
            chat_response = await simple_motorcycle_chat_agent_runner(message)
            message = chat_response.answer
            
        elif comparison_ids:
            self.logger.info(f"Session {session_id}: Comparison requested for IDs {comparison_ids}.")
            comparison_response = await self.compare_bikes(
                bike_ids=comparison_ids,
                user_message=original_user_message
            )
            message = comparison_response.get("answer", "")
            result.reasoning = comparison_response.get("reasoning", "")
            
            return {
                "answer": message,
                "reasoning": result.reasoning,
                "rows": comparison_response.get("rows", []),
                "session_id": session_id,
                "sql_query": None
            }
            
        
        
        return {
            "answer": message,
            "reasoning": result.reasoning,
            "rows": [],
            "session_id": session_id,
            "sql_query": None
        }
        
    async def compare_bikes(self, bike_ids: list[int], user_message: str) -> dict:
        
        if not bike_ids or len(bike_ids) < 2:
            return {"error": "Devi fornire almeno due IDs di moto per il confronto."}
        elif len(bike_ids) > 5:
            return {"error": "Puoi confrontare al massimo tre moto alla volta."}
        
        bikes = self.get_bikes_by_ids(bike_ids)
        
        comparation_response = await comparator_agent_runner(
            user_message=user_message,
            items=bikes,
            meta={"session_id": None}
        )
        
        return {
            "answer": comparation_response.answer,
            "reasoning": comparation_response.reasoning,
            "rows": bikes,
            "session_id": None,
            "sql_query": None
        }
    
    def get_bikes_by_ids(self, bike_ids: list[int]) -> list[dict]:
        """
        Recupera le moto dal database dato un elenco di IDs.
        Args:
            bike_ids: Lista di IDs delle moto da recuperare
        Returns:
            Lista di dizionari contenenti i dati delle moto
        """
        try:
            sql_query = f"SELECT * FROM motorcycles WHERE id IN ({', '.join(map(str, bike_ids))})"
            return self.queryExecutorSvc.execute_query(sql_query)
        except Exception as e:
            self.logger.error(f"Errore nel recupero delle moto per IDs {bike_ids}: {str(e)}")
            return []
        
        
            
            
        
        
        
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



