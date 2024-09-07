from sqlalchemy.orm import Session
from uuid import UUID
from app.models import User
from app.schemas import UserCreate
from app.security import get_password_hash

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: UUID):
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = User(username=user.username, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
