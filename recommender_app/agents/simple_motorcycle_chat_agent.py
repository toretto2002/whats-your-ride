"""
Simple Motorcycle Chat Agent
"""

from openai import OpenAI
from agents import Agent
from agents.run import Runner
from pydantic import BaseModel


class ChatOutput(BaseModel):
    answer: str
    
    
simple_motorcycle_chat_agent = Agent(
    name="Simple Motorcycle Chat Agent",
    instructions="""Sei un esperto di motociclette. Rispondi alle domande degli utenti in modo chiaro e conciso, fornendo informazioni accurate e pertinenti sul mondo delle moto. Usa un tono amichevole e professionale. Se non conosci la risposta, ammettilo onestamente. Non inventare informazioni. NON RISPONDERE A DOMANDE CHE NON RIGUARDANO LE MOTOCICLETTE. Se la domanda non riguarda le moto, rispondi semplicemente: "Mi dispiace, non posso aiutarti con questa domanda. Sono qui per parlare di motociclette.""",
    output_type=ChatOutput,
)  

async def simple_motorcycle_chat_agent_runner(input: str) -> ChatOutput:
    runner = Runner()
    result = await runner.run(starting_agent=simple_motorcycle_chat_agent, input=input)
    return result.final_output_as(ChatOutput)