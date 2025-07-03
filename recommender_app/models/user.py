from recommender_app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum as SQLEnum
from recommender_app.core.enums.role_enums import UserRole

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(SQLEnum(UserRole, name="user_role_enum"), nullable=False, default=UserRole.USER)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    surname = db.Column(db.String(100), nullable=True)
    birth_date = db.Column(db.Date, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)


    