"""
Ollama Motorcycle Query Agent (Local Model)

Questo agente sostituisce BotService che usa Ollama locale.
Usa modelli locali invece di OpenAI per privacy/costi.

Deve:
1. Usare modello Ollama locale (phi o altro)
2. Generare query SQL dalla domanda dell'utente
3. Eseguire la query sul database motorcycles
4. Restituire la risposta

NOTA: Questo agente potrebbe rimanere con llama-index se vuoi mantenere
      il supporto per modelli locali Ollama. In tal caso, mantieni la
      dipendenza llama-index-llms-ollama e llama-index-embeddings-ollama.

Alternative:
- Implementare con openai-agents + endpoint Ollama compatibile OpenAI
- Implementare chiamate dirette HTTP a Ollama API
- Mantenere llama-index solo per questo use case

Esempio uso:
    agent = OllamaMotorcycleQueryAgent(ollama_url="http://ollama:11434")
    result = await agent.query("Cerca naked leggere")
"""

# TODO: Decidere se:
# 1. Mantenere llama-index per Ollama
# 2. Usare Ollama OpenAI-compatible endpoint
# 3. Chiamate HTTP dirette


class OllamaMotorcycleQueryAgent:
    """
    Agent che usa Ollama locale per query su motorcycles.
    
    Sostituisce:
    - BotService (se si vuole eliminare llama-index completamente)
    
    NOTA: Può essere mantenuto con llama-index se necessario.
    """
    
    def __init__(
        self,
        database_engine,
        ollama_base_url: str = "http://ollama:11434",
        model: str = "phi"
    ):
        """
        Args:
            database_engine: SQLAlchemy engine
            ollama_base_url: URL base di Ollama
            model: Nome del modello Ollama da usare
        """
        self.engine = database_engine
        self.ollama_url = ollama_base_url
        self.model = model
        
        # TODO: Implementare connessione a Ollama
        
    async def query(self, user_question: str) -> str:
        """
        Processa una query usando Ollama locale.
        
        Args:
            user_question: Domanda dell'utente
            
        Returns:
            str: Risposta generata
        """
        # TODO: Implementare
        raise NotImplementedError("Da implementare")


# ALTERNATIVE: Se vuoi mantenere llama-index per Ollama
class OllamaMotorcycleQueryAgentWithLlamaIndex:
    """
    Versione che mantiene llama-index per Ollama locale.
    
    Questa è una soluzione ibrida:
    - OpenAI agents per servizi cloud OpenAI
    - llama-index per modelli locali Ollama
    """
    pass
