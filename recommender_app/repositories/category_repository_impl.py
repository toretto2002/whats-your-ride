from recommender_app.interfaces.category_repository import CategoryRepository
from recommender_app.models.category import Category
from typing import List, Optional

class CategoryRepositoryImpl(CategoryRepository):
    
    def __init__(self, db_session):
        self.db_session = db_session

    def get_category(self, category_id: str) -> Optional[Category]:
        """Get a category by its ID."""
        return self.db_session.query(Category).filter(Category.id == category_id).first()

    def list_categories(self) -> List[Category]:
        """List all categories."""
        return self.db_session.query(Category).all()

    def create_category(self, category: Category) -> None:
        """Create a new category."""
        self.db_session.add(category)
        self.db_session.commit()

    def update_category(self, category: Category) -> None:
        """Update an existing category."""
        existing_category = self.get_category(category.id)
        if not existing_category:
            raise ValueError(f"Category with ID {category.id} does not exist.")
        self.db_session.commit()

    def delete_category(self, category_id: str) -> None:
        """Delete a category by its ID."""
        category = self.get_category(category_id)
        if category:
            self.db_session.delete(category)
            self.db_session.commit()