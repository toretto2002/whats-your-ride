from recommender_app.interfaces.brand_repository import BrandRepository
from recommender_app.models.brand import Brand
from typing import List, Optional

class BrandRepositoryImpl(BrandRepository):

    def __init__(self, db_session):
        self.db_session = db_session

    def get_brand_by_name(self, name: str) -> Brand:
        return self.db_session.query(Brand).filter(Brand.name == name).first()

    def save_brand(self, brand: Brand) -> int:
        self.db_session.add(brand)
        self.db_session.commit()
        self.db_session.refresh(brand)
        return brand.id

    def get_all_brands(self) -> List[Brand]:
        return self.db_session.query(Brand).all()