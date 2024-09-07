from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import FeedbackCreate
from app.repositories.feedback_repository import FeedbackRepository

class FeedbackService:
    def __init__(self, db: Session):
        self.feedback_repository = FeedbackRepository(db)

    def create_feedback(self, feedback: FeedbackCreate, note_id: UUID, user_id: UUID):
        return self.feedback_repository.create_feedback(feedback, note_id, user_id)

    def get_feedback(self, note_id: UUID):
        return self.feedback_repository.get_feedback(note_id)
