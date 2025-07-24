from recommender_app.models.model import Model
from recommender_app.schemas.model_dto import ModelCreate, ModelOut

class ModelService:
    def __init__(self, db_session):
        self.db_session = db_session

    def save_model(self, model_data) -> int:
        """
        Save a motorcycle model to the database.
        """
        new_model = Model(**model_data)
        self.db_session.add(new_model)
        self.db_session.commit()
        self.db_session.refresh(new_model)
        return new_model.id

    def get_model_by_id(self, model_id) -> ModelOut:
        """
        Retrieve a motorcycle model by its ID.
        """
        return self.db_session.query(Model).filter_by(id=model_id).first()