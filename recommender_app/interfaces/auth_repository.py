from typing import Optional, Protocol
from recommender_app.schemas.auth_dto import AuthBase

class UserRepository(Protocol):
    def get_user_login_by_username(username: str) -> Optional[AuthBase]:
        """Retrieve a user login by their username."""
        pass