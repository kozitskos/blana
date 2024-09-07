from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import SummaryCreate, Summary
from app.services.summary_service import SummaryService
from app.deps import get_db, get_current_user
from app.schemas import User

router = APIRouter()

@router.post("/{note_id}/summary", response_model=Summary)
def create_summary(
    note_id: UUID,
    summary: SummaryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    summary_service = SummaryService(db)
    return summary_service.create_summary(summary, note_id, current_user.id)

@router.get("/{note_id}/summary", response_model=Summary)
def get_summary_for_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    summary_service = SummaryService(db)
    summary = summary_service.get_summary_for_note(note_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary
