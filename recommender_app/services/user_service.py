
from ..repositories.user_repositor_impl import UserRepositoryImpl
from ..schemas.registration_dto import UserRegistration, UserOut, UserUpdate

class UserService:

    def __init__(self):
        self.user_repository = UserRepositoryImpl()

    def create_user(self, user: UserRegistration) -> UserOut:
        return self.user_repository.create(user)

    def get_user_by_id(self, user_id: int) -> UserOut:
        return self.user_repository.get_user_by_id(user_id)

    def update_user(self, user_id: int, user_update: UserUpdate) -> UserOut:
        return self.user_repository.update_user(user_id, user_update)

    def delete_user(self, user_id: int) -> None:
        return self.user_repository.delete(user_id)

    def list_users(self) -> list[UserOut]:
        return self.user_repository.list_all()
