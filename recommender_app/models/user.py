from recommender_app.extensions import db

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    surname = db.Column(db.String(100), nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
