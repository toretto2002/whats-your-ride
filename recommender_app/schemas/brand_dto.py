from pydantic import BaseModel, Field

class BrandBase(BaseModel):
    name: str
    url: str

class BrandCreate(BrandBase):
    pass

class BrandOut(BrandBase):
    id: int

    class Config:
        orm_mode = True

class BrandWithModels(BrandOut):
    models: list[str]

    class Config:
        orm_mode = True
        from_attributes = True
