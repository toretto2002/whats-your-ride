from recommender_app.models.user import User
from recommender_app.interfaces.user_repository import UserRepository
from recommender_app.schemas.registration_dto import UserRegistration, UserUpdate, UserOut
from recommender_app.extensions import db 

class UserRepositoryImpl(UserRepository):

    def get_by_id(self, user_id: int) -> UserOut:
        user = User.query.get(user_id)
        return UserOut.model_validate(user) if user else None

    def get_by_username(self, username: str) -> UserOut:
        user = User.query.filter_by(username=username).first()
        return UserOut.model_validate(user) if user else None

    def create(self, user_in: UserRegistration) -> UserOut:
        user = User(**user_in.dict(exclude={'password'}))
        user.set_password(user_in.password)
        db.session.add(user)
        db.session.commit()
        return UserOut.model_validate(user)

    def update(self, user_id: int, user_in: UserUpdate) -> UserOut:
        user = User.query.get(user_id)
        if not user:
            return None
        for field, value in user_in.dict(exclude_unset=True).items():
            if field == "password":
                user.set_password(value)
            else:
                setattr(user, field, value)
        db.session.commit()
        return UserOut.model_validate(user)

    def delete(self, user_id: int) -> None:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    def list_all(self) -> list[UserOut]:
        users = User.query.all()
        return [UserOut.model_validate(u) for u in users]
