from recommender_app.repositories.category_repository_impl import CategoryRepositoryImpl

class CategoryService:
    
    def __init__(self):
        self.category_repository = CategoryRepositoryImpl()

    def create_category(self, category: dict) -> dict:
        return self.category_repository.create(category)

    def get_category_by_id(self, category_id: int) -> dict:
        return self.category_repository.get_by_id(category_id)

    def update_category(self, category_id: int, category_update: dict) -> dict:
        return self.category_repository.update(category_id, category_update)

    def delete_category(self, category_id: int) -> None:
        return self.category_repository.delete(category_id)

    def list_categories(self) -> list[dict]:
        return self.category_repository.list_all()
