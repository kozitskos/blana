from sqlalchemy.orm import Session
from uuid import UUID
from app.models import Feedback
from app.schemas import FeedbackCreate

class FeedbackRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_feedback(self, feedback: FeedbackCreate, note_id: UUID, user_id: UUID):
        db_feedback = Feedback(**feedback.dict(), note_id=note_id, author_id=user_id)
        self.db.add(db_feedback)
        self.db.commit()
        self.db.refresh(db_feedback)
        return db_feedback

    def get_feedback(self, note_id: UUID):
        return self.db.query(Feedback).filter(Feedback.note_id == note_id).first()
