"""
Answer Synthesis Agent

Questo agente sostituisce la logica di sintesi delle risposte.
Deve:
1. Prendere i risultati della query SQL (lista di dizionari)
2. Considerare lo storico della conversazione
3. Generare una risposta naturale e conversazionale
4. Formattare tabelle, statistiche e insights
5. Gestire casi con 0 risultati o troppi risultati

Dipendenze OpenAI Agents:
- Agent base class
- Data formatting tools
- Conversation history context

Esempio uso:
    agent = AnswerSynthesisAgent()
    answer = await agent.synthesize(
        user_question="Cerco una naked leggera",
        sql_query="SELECT * FROM versions_enriched WHERE...",
        results=[{...}, {...}],
        conversation_history=[...]
    )

Template prompt:
- Vedi: utils/prompts/moto_it/user_prompt_template.txt
- Vedi: utils/prompts/moto_it/answer_llm_system_prompt.txt
"""

from openai import OpenAI
# TODO: Implementare con openai-agents
from agents import Agent, Task


class AnswerSynthesisAgent:
    """
    Agent che sintetizza risposte naturali dai risultati SQL.
    
    Sostituisce:
    - MotoItOpenAiBotService._synthesize_answer()
    - AnswerBotService.compress_results()
    - Logica di formattazione risposta
    """
    
    def __init__(self, max_table_rows: int = 10):
        """
        Args:
            max_table_rows: Numero massimo di righe da mostrare nelle tabelle
        """
        self.max_table_rows = max_table_rows
        # TODO: Inizializzare OpenAI Agent
        
    async def synthesize(
        self,
        user_question: str,
        sql_query: str,
        results: list[dict],
        conversation_history: list[dict] = None
    ) -> str:
        """
        Genera una risposta naturale dai risultati SQL.
        
        Args:
            user_question: Domanda originale dell'utente
            sql_query: Query SQL eseguita
            results: Risultati della query (lista di dizionari)
            conversation_history: Storico della conversazione
            
        Returns:
            str: Risposta formattata in linguaggio naturale
        """
        # TODO: Implementare logica con openai-agents
        raise NotImplementedError("Da implementare con openai-agents")
    
    def _compress_results(self, results: list[dict], user_question: str) -> dict:
        """
        Comprime i risultati per ridurre i token inviati al modello.
        
        Args:
            results: Risultati completi
            user_question: Domanda dell'utente per contestualizzare
            
        Returns:
            dict: Payload compresso con tabelle, stats, gruppi
        """
        # TODO: Implementare compressione intelligente
        raise NotImplementedError("Da implementare")
    
    def _summarize_history(self, history: list[dict]) -> str:
        """
        Riassume lo storico conversazione per risparmiare token.
        
        Args:
            history: Lista di messaggi [{role, content}, ...]
            
        Returns:
            str: Riassunto dello storico
        """
        # TODO: Implementare summarization
        raise NotImplementedError("Da implementare")
