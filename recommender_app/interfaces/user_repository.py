from typing import Protocol, List, Optional
from recommender_app.schemas.registration_dto import UserRegistration, UserOut, UserUpdate

class UserRepository(Protocol):
    def create_user(self, user: UserRegistration) -> UserOut:
        """Create a new user in the repository."""
        pass    

    def get_user_by_id(self, user_id: int) -> Optional[UserOut]:
        """Retrieve a user by their ID."""
        pass

    def get_user_by_username(self, username: str) -> Optional[UserOut]:
        """Retrieve a user by their username."""
        pass

    def update_user(self, user_id: int, user_update: UserUpdate) -> UserOut:
        """Update an existing user's information."""
        pass

    def delete_user(self, user_id: int) -> None:
        """Delete a user from the repository."""
        pass

    def list_users(self) -> List[UserOut]:
        """List all users in the repository."""
        pass