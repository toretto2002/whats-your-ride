from recommender_app.repositories.category_repository_impl import CategoryRepositoryImpl
from recommender_app.schemas.category_dto import CategoryCreate, CategoryOut
from typing import Optional, List

class CategoryService:
    
    def __init__(self):
        self.category_repository = CategoryRepositoryImpl()

    def create_category(self, category: dict) -> int:
        return self.category_repository.create_category(category)

    def get_category_by_id(self, category_id: int) -> CategoryOut:
        return self.category_repository.get_by_id(category_id)
    
    def get_category_by_name(self, name: str) -> Optional[CategoryOut]:
        return self.category_repository.get_category_by_name(name)

    def update_category(self, category_id: int, category_update: dict) -> dict:
        return self.category_repository.update(category_id, category_update)

    def delete_category(self, category_id: int) -> None:
        return self.category_repository.delete(category_id)

    def list_categories(self) -> list[CategoryOut]:
        return self.category_repository.list_categories()
