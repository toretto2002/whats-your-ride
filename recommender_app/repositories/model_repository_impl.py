from recommender_app.interfaces.model_repository import ModelRepository
from recommender_app.models.model import Model
from typing import List, Optional

class ModelRepositoryImpl(ModelRepository):

    def __init__(self, db_session):
        self.db_session = db_session

    def create_model(self, dto) -> None:
        """Create a new model."""
        new_model = Model(**dto)
        self.db_session.add(new_model)
        self.db_session.commit()

    def get_model(self, model_id: int) -> Optional[Model]:
        """Get a model by its ID."""
        return self.db_session.query(Model).filter(Model.id == model_id).first()

    def update_model(self, model_id: int, name: str, brand_id: int, url: str) -> None:
        """Update an existing model."""
        model = self.get_model(model_id)
        if model:
            model.name = name
            model.brand_id = brand_id
            model.url = url
            self.db_session.commit()

    def delete_model(self, model_id: int) -> None:
        """Delete a model by its ID."""
        model = self.get_model(model_id)
        if model:
            self.db_session.delete(model)
            self.db_session.commit()

    def get_all_models(self) -> List[Model]:
        """Get all models."""
        return self.db_session.query(Model).all()