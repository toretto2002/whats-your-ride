from typing import Protocol, List, Optional
from recommender_app.models.category import Category

class CategoryRepository(Protocol):
    def get_category(self, category_id: str) -> Optional[Category]:
        """Get a category by its ID."""
        pass

    def list_categories(self) -> List[Category]:
        """List all categories."""
        pass

    def create_category(self, category: Category) -> None:
        """Create a new category."""
        pass

    def update_category(self, category: Category) -> None:
        """Update an existing category."""
        pass

    def delete_category(self, category_id: str) -> None:
        """Delete a category by its ID."""
        pass
    
    def get_category_by_name(self, name: str) -> Optional[Category]:
        """Get a category by its name."""
        pass
    
    