from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from recommender_app.core.enums.role_enums import UserRole

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