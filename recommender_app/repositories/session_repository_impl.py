from recommender_app.interfaces.session_repository import SessionRepository
from recommender_app.models.chat_session import ChatSession
from recommender_app.extensions import db
from sqlalchemy import desc
from recommender_app.models.chat_message import ChatMessage

class SessionRepositoryImpl(SessionRepository):
    
    def create_session(self, session) -> int:
        db.session.add(session)
        db.session.commit()
        db.session.refresh(session)
        return session.id

    def get_session_by_id(self, session_id: int) -> ChatSession | None:
        return db.session.query(ChatSession).filter(ChatSession.id == session_id).first()
    
    def update_session(self, session: ChatSession) -> None:
        db.session.merge(session)
        db.session.commit()
        
    def get_history(self, session_id: int, limit: int | None = None) -> list[ChatMessage]:
        query = (
            db.session.query(ChatMessage)
            .filter(ChatMessage.chat_session_id == session_id)
            .order_by(ChatMessage.timestamp.asc())
        )
        if limit:
            query = query.limit(limit)
        return query.all()