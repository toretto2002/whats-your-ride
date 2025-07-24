from pydantic import BaseModel
from recommender_app.schemas.model_dto import ModelOut

class CategoryBase(BaseModel):
    name: str
    description: str

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class CategoryWithModels(CategoryOut):
    models: list[ModelOut]

    class Config:
        orm_mode = True
        from_attributes = True