from recommender_app.extensions import db

class Brand(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    models = db.relationship('Model', backref='brand', lazy=True)