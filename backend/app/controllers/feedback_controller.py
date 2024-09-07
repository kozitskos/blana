from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import FeedbackCreate, Feedback
from app.services.feedback_service import FeedbackService
from app.deps import get_db, get_current_user
from app.schemas import User

router = APIRouter()

@router.post("/{note_id}/feedback", response_model=Feedback)
def create_feedback(
    note_id: UUID,
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    feedback_service = FeedbackService(db)
    return feedback_service.create_feedback(feedback, note_id, current_user.id)

@router.get("/{note_id}/feedback", response_model=Feedback)
def get_feedback_for_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    feedback_service = FeedbackService(db)
    feedback = feedback_service.get_feedback_for_note(note_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback
