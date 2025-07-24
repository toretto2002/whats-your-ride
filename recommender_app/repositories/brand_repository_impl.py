from recommender_app.interfaces.brand_repository import BrandRepository
from recommender_app.models.brand import Brand
from typing import List, Optional
from recommender_app.extensions import db  

class BrandRepositoryImpl(BrandRepository):

    def get_brand_by_name(self, name: str) -> Brand:
        return db.session.query(Brand).filter(Brand.name == name).first()

    def save_brand(self, brand: Brand) -> int:
        db.session.add(brand)
        db.session.commit()
        db.session.refresh(brand)
        return brand.id

    def get_all_brands(self) -> List[Brand]:
        return db.session.query(Brand).all()