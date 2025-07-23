from recommender_app.extensions import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    models = db.relationship('Model', backref='category', lazy=True)
