from recommender_app.models.model import Model
from recommender_app.schemas.model_dto import ModelCreate, ModelOut
from recommender_app.repositories.model_repository_impl import ModelRepositoryImpl

class ModelService:
    
    def __init__(self):
        self.model_repository = ModelRepositoryImpl()

    def save_model(self, model_data) -> int:
        return self.model_repository.create_model(model_data)

    def get_model_by_id(self, model_id) -> ModelOut:
        return self.model_repository.get_model(model_id)
    
    def get_or_create_model(self, model_data: dict) -> int:
        return self.model_repository.get_or_create_model(model_data)
    
    