from pydantic import BaseModel

class MessageCreate(BaseModel):
    session_id: int
    sender: str 
    message: str
    timestamp: str  
    
class MessageOut(MessageCreate):
    id: int

    class Config:
        orm_mode = True