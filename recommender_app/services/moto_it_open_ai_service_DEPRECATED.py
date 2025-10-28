"""
DEPRECATO: Questo servizio è stato rimosso e sostituito con openai-agents.

Usare invece:
- recommender_app.agents.motorcycle_recommendation_orchestrator_agent.MotorcycleRecommendationOrchestrator

Questo file contiene il codice originale per referenza durante la migrazione.
"""

# Il codice originale è stato spostato qui per referenza.
# Vedere gli agenti in recommender_app/agents/ per la nuova implementazione.

class MotoItOpenAiBotService:
    """DEPRECATO - Non usare"""
    
    def __init__(self):
        raise NotImplementedError(
            "Servizio deprecato. Usare MotorcycleRecommendationOrchestrator da "
            "recommender_app.agents.motorcycle_recommendation_orchestrator_agent"
        )
    
    def ask(self, message: str, session_id: int | None = None) -> dict:
        raise NotImplementedError("Deprecato")
