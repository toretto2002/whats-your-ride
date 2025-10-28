"""DEPRECATO - Usare openai-agents invece."""
import logging
from recommender_app.agents.sql_rag_gate_agent import sql_rag_gate_agent_runner
from recommender_app.agents.sql_query_generator_agent import sql_query_generator_agent_runner, refresh_sql_query_generator_agent_categories
from recommender_app.agents.simple_motorcycle_chat_agent import simple_motorcycle_chat_agent_runner
from recommender_app.services.category_service import CategoryService



class MotoItOpenAiBotService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.categorySvc = CategoryService()
    
    async def ask(self, message: str, session_id: int | None = None) -> dict:
        result = await sql_rag_gate_agent_runner(message)
        
        if result.is_sql_query:
            self.logger.info(f"Session {session_id}: SQL query needed. Reasoning: {result.reasoning}")
            categories_tuples = self.categorySvc.list_categories_as_tuples()
            refresh_sql_query_generator_agent_categories(categories_tuples)            
            sql = await sql_query_generator_agent_runner(message)
            message = f"Esegui la seguente query SQL per ottenere le informazioni richieste:\n{sql.sql_query}"
            
        else:
            self.logger.info(f"Session {session_id}: No SQL query needed. Reasoning: {result.reasoning}")
            chat_response = await simple_motorcycle_chat_agent_runner(message)
            message = chat_response.answer
        
        return {
            "answer": message,
            "reasoning": result.reasoning,
            "rows": [],
            "session_id": session_id,
            "sql_query": sql.sql_query if result.is_sql_query else None
        }



