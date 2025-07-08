from ..repositories.auth_repository_impl import AuthRepositoryImpl
from recommender_app.core.security import verify_password


class AuthService:
        

    @staticmethod
    def login_user(username: str, password: str):
        user_repository = AuthRepositoryImpl()
        user = user_repository.get_user_login_by_username(username)
        print(f"User found: {user}")
        if user and verify_password(user.password, password):
            return user
        return None