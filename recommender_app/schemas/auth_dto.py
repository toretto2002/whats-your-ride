from pydantic import BaseModel, EmailStr
from typing import Optional

class AuthBase(BaseModel):
    username: str
    password: str
