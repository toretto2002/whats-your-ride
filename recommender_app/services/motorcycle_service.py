from recommender_app.extensions import db
from recommender_app.models.motorcycle import Motorcycle

def save_bike_data_on_db( data: dict):

    m = Motorcycle(**data)
    db.session.add(m)
    db.session.commit()