

from typing import Protocol
from recommender_app.schemas.message_dto import MessageCreate, MessageOut


class MessageRepository(Protocol):

    def create_message(self, message: MessageCreate) -> int:
        """Create a new message."""
        pass

    def get_messages_by_session_id(self, session_id: int) -> list[MessageOut]:
        """Retrieve messages by session ID."""
        pass