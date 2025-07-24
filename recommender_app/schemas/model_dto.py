from pydantic import BaseModel

class ModelBase(BaseModel):
    name: str
    description: str
    category_id: int
    brand_id: int
    lower_price: float
    upper_price: float

class ModelCreate(ModelBase):
    pass

class ModelOut(ModelBase):
    id: int

    class Config:
        orm_mode = True

class ModelWithDetails(ModelOut):
    category_name: str
    brand_name: str

    class Config:
        orm_mode = True
        from_attributes = True
