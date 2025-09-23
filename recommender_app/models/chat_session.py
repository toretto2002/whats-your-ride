
import datetime
from recommender_app.extensions import db

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.datetime.now)
    ended_at = db.Column(db.DateTime, nullable=True)
    messages = db.relationship('ChatMessage', backref='chat_session', lazy=True)
        