from typing import Protocol, List, Optional
from recommender_app.models.model import Model

class ModelRepository(Protocol):

    def create_model(self, name: str, brand_id: int, url: str) -> None:
        """Create a new model."""
        pass

    def get_model(self, model_id: int) -> Optional[Model]:
        """Get a model by its ID."""
        pass

    def update_model(self, model_id: int, name: str, brand_id: int, url: str) -> None:
        """Update an existing model."""
        pass

    def delete_model(self, model_id: int) -> None:
        """Delete a model by its ID."""
        pass

    def get_all_models(self) -> List[Model]:
        """Get all models."""
        pass
    
    def get_model_by_name(self, name: str) -> Optional[Model]:
        """Get a model by its name."""
        pass
    
    def get_or_create_model(self, model_data: dict) -> int:
        """Get an existing model or create a new one."""
        pass