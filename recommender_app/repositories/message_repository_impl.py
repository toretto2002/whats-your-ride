
from recommender_app.interfaces.message_repository import MessageRepository
from recommender_app.schemas.message_dto import MessageCreate, MessageOut
from recommender_app.extensions import db


class MessageRepositoryImpl(MessageRepository):
    
    def create_message(self, message: MessageCreate) -> int:
        db.session.add(message)
        db.session.commit()
        db.session.refresh(message)
        return message.id

    def get_messages_by_session_id(self, session_id: int) -> list:
        return db.session.query(MessageOut).filter(MessageOut.session_id == session_id).all()