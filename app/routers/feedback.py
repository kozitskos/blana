from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from .. import schemas, crud
from ..database import get_db
from ..deps import get_current_user

router = APIRouter()

@router.post("/{note_id}/feedback/", response_model=schemas.Feedback)
def create_feedback_for_note(
    note_id: UUID,
    feedback: schemas.FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    note = crud.get_note_by_id(db, note_id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to provide feedback on this note")
    return crud.create_feedback(db=db, feedback=feedback, note_id=note_id, user_id=current_user.id)

@router.get("/{note_id}/feedback/", response_model=schemas.Feedback)
def read_feedback(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    feedback = crud.get_feedback(db, note_id=note_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    if feedback.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this feedback")
    return feedback
