from sqlalchemy.orm import Session
from uuid import UUID
from . import models, schemas
from .security import get_password_hash, verify_password

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id(db: Session, user_id: UUID):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_notes(db: Session, user_id: UUID):
    return db.query(models.Note).filter(models.Note.owner_id == user_id).all()

def create_user_note(db: Session, note: schemas.NoteCreate, user_id: UUID):
    db_note = models.Note(**note.dict(), owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_note_by_id(db: Session, note_id: UUID):
    return db.query(models.Note).filter(models.Note.id == note_id).first()

def update_note_content(db: Session, note_id: UUID, content: str):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note:
        note.content = content
        db.commit()
        db.refresh(note)
    return note

def create_feedback(db: Session, feedback: schemas.FeedbackCreate, note_id: UUID, user_id: UUID):
    db_feedback = models.Feedback(**feedback.dict(), note_id=note_id, author_id=user_id)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback
