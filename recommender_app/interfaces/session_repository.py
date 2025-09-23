from typing import Protocol
from recommender_app.schemas.session_dto import ChatSessionCreate, ChatSessionOut

class SessionRepository(Protocol):

    def create_session(self, session: ChatSessionCreate) -> int:
        """Create a new session for a user."""
        pass

    def get_session_by_id(self, session_id: int) -> ChatSessionOut | None:
        """Retrieve a session by its ID."""
        pass

    def update_session(self, session: ChatSessionOut) -> None:
        """Update an existing session."""
        pass
    
    