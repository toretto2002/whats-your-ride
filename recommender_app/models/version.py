from recommender_app.extensions import db

class Version(db.Model):
    __tablename__ = 'versions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'), nullable=False)
