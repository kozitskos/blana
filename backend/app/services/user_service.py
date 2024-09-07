from sqlalchemy.orm import Session
from app.schemas import UserCreate
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def create_user(self, user: UserCreate):
        return self.user_repository.create_user(user)

    def get_user_by_username(self, username: str):
        return self.user_repository.get_user_by_username(username)

    def get_user_by_id(self, user_id: UUID):
        return self.user_repository.get_user_by_id(user_id)
