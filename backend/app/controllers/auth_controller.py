from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.schemas import Token, UserCreate, User
from app.database import get_db
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/token", response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    auth_service = AuthService(db)
    access_token = auth_service.login_user(form_data.username, form_data.password)
    
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    db_user = auth_service.create_user(user)
    
    if not db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    return db_user
