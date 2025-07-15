from recommender_app.models.motorcycle import Motorcycle
from recommender_app.interfaces.motorcycle_repository import MotorcycleRepository

class MotorcycleRepositoryImpl(MotorcycleRepository):

    def get_motorcycle_by_id(self, motorcycle_id: int) -> Optional[Motorcycle]:
        return self.db_session.query(Motorcycle).filter(Motorcycle.id == motorcycle_id).first()

    def add_motorcycle(self, motorcycle: Motorcycle):
        self.db_session.add(motorcycle)
        self.db_session.commit()

    def update_motorcycle(self, motorcycle: Motorcycle):
        existing_motorcycle = self.get_motorcycle_by_id(motorcycle.id)
        if existing_motorcycle:
            for key, value in motorcycle.__dict__.items():
                setattr(existing_motorcycle, key, value)
            self.db_session.commit()
        else:
            raise ValueError("Motorcycle not found")

    def delete_motorcycle(self, motorcycle_id: int):
        motorcycle = self.get_motorcycle_by_id(motorcycle_id)
        if motorcycle:
            self.db_session.delete(motorcycle)
            self.db_session.commit()
        else:
            raise ValueError("Motorcycle not found")