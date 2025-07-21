from recommender_app.extensions import db
from recommender_app.models.motorcycle import Motorcycle

def save_bike_data_on_db( data: dict):

    exists = db.session.query(Motorcycle).filter_by(source_url=data['source_url']).first()
    if exists:
        print(f"Skip model already in DB: {data['full_name']}")
        return

    bike = Motorcycle(**data)
    db.session.add(bike)
    db.session.commit()