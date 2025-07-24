from recommender_app.models.brand import Brand
from recommender_app.repositories.brand_repository_impl import BrandRepositoryImpl


class BrandService:

    def __init__(self):
        self.brand_repository = BrandRepositoryImpl()


    def create_brand(self, dto: dict) -> int:
        """Create a new brand."""
        brand = self.brand_repository.get_brand_by_name(dto["name"])
        if brand:
            raise ValueError(f"Brand {dto['name']} already exists.")

        new_brand = Brand(**dto)
        return self.brand_repository.save_brand(new_brand)





