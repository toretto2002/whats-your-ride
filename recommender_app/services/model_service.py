from recommender_app.models.model import Model

class ModelService:
    def __init__(self, db_session):
        self.db_session = db_session

    def save_model(self, model_data):
        """
        Save a motorcycle model to the database.
        """
        new_model = Model(**model_data)
        self.db_session.add(new_model)
        self.db_session.commit()
        return new_model

    def get_model_by_id(self, model_id):
        """
        Retrieve a motorcycle model by its ID.
        """
        return self.db_session.query(Model).filter_by(id=model_id).first()