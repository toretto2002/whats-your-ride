from ..repositories.user_repositor_impl import UserRepositoryImpl
from recommender_app.core.security import verify_password


class AuthService:
        

    @staticmethod
    def login_user(username: str, password: str):
        user_repository = UserRepositoryImpl()
        user = user_repository.get_user_by_username(username)
        print(f"User found: {user}")
        if user and verify_password(user.password_hash, password):
            return user
        return None