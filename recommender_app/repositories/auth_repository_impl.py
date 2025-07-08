from recommender_app.interfaces.auth_repository import AuthRepository
from recommender_app.models.user import User
from recommender_app.schemas.auth_dto import AuthBase
from typing import Optional

class AuthRepositoryImpl(AuthRepository):

    def get_user_login_by_username(self, username: str) -> Optional[AuthBase]:
        """Retrieve a user login by their username."""
        user = User.query.filter_by(username=username).first()
        if user:
            return AuthBase(id=user.id, username=user.username, password=user.password_hash, role=user.role)
        return None

