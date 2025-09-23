from pydantic import BaseModel
from recommender_app.schemas.message_dto import MessageOut

class ChatSessionBase(BaseModel):
    user_id: int
    started_at: str  
    ended_at: str | None = None  
    messages: list[MessageOut]
    
class ChatSessionCreate(ChatSessionBase):
    pass  

class ChatSessionOut(ChatSessionBase):
    id: int

    class Config:
        orm_mode = True