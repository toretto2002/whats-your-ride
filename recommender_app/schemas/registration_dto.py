from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    username: str
    role: UserRole = UserRole.USER
    name: str
    surname: str
    email: EmailStr
    birth_date: date

    class Config:
        from_attributes = True

class UserRegistration(UserBase):
    password: str

class UserOut(UserBase):
    id: int

class UserUpdate(UserBase):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    surname: Optional[str]
    birth_date: Optional[date]
    role: Optional[str]