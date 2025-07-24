from recommender_app.interfaces.model_repository import ModelRepository
from recommender_app.models.model import Model
from typing import List, Optional
from recommender_app.extensions import db

class ModelRepositoryImpl(ModelRepository):


    def create_model(self, dto) -> int:
        """Create a new model."""
        new_model = Model(**dto)
        db.session.add(new_model)
        db.session.commit()
        db.session.refresh(new_model)
        return new_model.id

    def get_model(self, model_id: int) -> Optional[Model]:
        """Get a model by its ID."""
        return db.session.query(Model).filter(Model.id == model_id).first()

    def update_model(self, model_id: int, name: str, brand_id: int, url: str) -> None:
        """Update an existing model."""
        model = self.get_model(model_id)
        if model:
            model.name = name
            model.brand_id = brand_id
            model.url = url
            db.session.commit()

    def delete_model(self, model_id: int) -> None:
        """Delete a model by its ID."""
        model = self.get_model(model_id)
        if model:
            db.session.delete(model)
            db.session.commit()

    def get_all_models(self) -> List[Model]:
        """Get all models."""
        return db.session.query(Model).all()

    def get_or_create_model(self, model_data) -> int:
        existing_model = db.session.query(Model).filter_by(name=model_data["name"]).first()
        if existing_model:
            return existing_model.id  # usa l'id esistente
        model = Model(**model_data)
        db.session.add(model)
        db.session.commit()
        return model.id
