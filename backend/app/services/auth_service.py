from sqlalchemy.orm import Session
from datetime import timedelta
from app.schemas import UserCreate
from app.repositories.user_repository import UserRepository
from app.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from uuid import UUID

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def login_user(self, username: str, password: str) -> str:
        user = self.user_repository.get_user_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        return access_token

    def create_user(self, user: UserCreate):
        db_user = self.user_repository.get_user_by_username(user.username)
        if db_user:
            return None
        return self.user_repository.create_user(user)
