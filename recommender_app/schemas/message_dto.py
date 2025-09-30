from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MessageCreate(BaseModel):
    chat_session_id: int
    sender: str 
    message: str
    timestamp: datetime
    
class MessageOut(MessageCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)