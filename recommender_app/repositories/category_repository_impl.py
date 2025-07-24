from recommender_app.interfaces.category_repository import CategoryRepository
from recommender_app.models import category
from recommender_app.models.category import Category
from typing import List, Optional
from recommender_app.schemas.category_dto import CategoryCreate, CategoryOut, CategoryWithModels 
from recommender_app.extensions import db   

class CategoryRepositoryImpl(CategoryRepository):
    

    def get_category(self, category_id: str) -> Optional[CategoryOut]:
        """Get a category by its ID."""
        return db.session.query(Category).filter(Category.id == category_id).first()

    def list_categories(self) -> List[CategoryOut]:
        """List all categories."""
        return db.session.query(Category).all()

    def create_category(self, cat: dict) -> int:
        """Create a new category."""
        category = Category(**cat)
        db.session.add(category)
        db.session.commit()
        db.session.refresh(category)
        return category.id

    def update_category(self, category: Category) -> None:
        """Update an existing category."""
        existing_category = self.get_category(category.id)
        if not existing_category:
            raise ValueError(f"Category with ID {category.id} does not exist.")
        db.session.commit()

    def delete_category(self, category_id: str) -> None:
        """Delete a category by its ID."""
        category = self.get_category(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            
    def get_category_by_name(self, name: str) -> Optional[CategoryOut]:
        """Get a category by its name."""
        return db.session.query(Category).filter(Category.name == name).first()