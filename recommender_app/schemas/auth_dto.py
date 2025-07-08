from pydantic import BaseModel, EmailStr
from typing import Optional

class AuthBase(BaseModel):
    id: int
    username: str
    password: str
    role: str
