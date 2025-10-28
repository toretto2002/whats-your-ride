from agents import Agent, Runner
from pydantic import BaseModel

class TestOutput(BaseModel):
    result: str

agent = Agent(
    name="Test",
    instructions="Just say hello",
    output_type=TestOutput
)

print("Agent created:", agent)
print("Runner type:", type(Runner))
print("Runner:", Runner)
