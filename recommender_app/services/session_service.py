from recommender_app.repositories.session_repository_impl import SessionRepositoryImpl
from recommender_app.repositories.message_repository_impl import MessageRepositoryImpl
from recommender_app.models.chat_message import ChatMessage
from recommender_app.models.chat_session import ChatSession
from recommender_app.schemas.message_dto import MessageOut

class SessionService:
    
    def __init__(self):
        self.session_repository = SessionRepositoryImpl()
        self.message_repository = MessageRepositoryImpl()
        
    def create_session(self, user_id: int) -> str:
        session: ChatSession = ChatSession(
            user_id=user_id
        )
        
        return self.session_repository.create_session(session)
    
    def append_message(self, session_id: int, message_content: str, sender: str) -> None:
        session = self.session_repository.get_session_by_id(session_id)
        
        if not session:
            raise ValueError(f"Session with ID {session_id} does not exist.")
        
        message: ChatMessage = ChatMessage(
            chat_session_id=session_id,
            sender = sender,
            message = message_content,
        )
        
        message.id = self.message_repository.create_message(message)
        
        session.messages.append(message)
        self.session_repository.update_session(session)
        
    def get_messages(self, session_id: int, limit: int = 10) -> list[MessageOut]:
        session = self.session_repository.get_session_by_id(session_id)
        
        if not session:
            raise ValueError(f"Session with ID {session_id} does not exist.")
        
        # Fetch at most `limit` messages from the repository (ordered by timestamp ASC there)
        messages = self.session_repository.get_history(session_id, limit=limit)
        return [MessageOut.from_orm(m) for m in messages]
