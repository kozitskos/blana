from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from .. import schemas, crud
from ..database import get_db
from ..deps import get_current_user

router = APIRouter()

@router.post("/{note_id}/summary/", response_model=schemas.Summary)
def create_or_update_summary_for_note(
    note_id: UUID,
    summary: schemas.SummaryCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    note = crud.get_note_by_id(db, note_id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to provide summary for this note")
    return crud.create_summary(db=db, summary=summary, note_id=note_id, user_id=current_user.id)

@router.get("/{note_id}/summary/", response_model=schemas.Summary)
def read_summary(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    note = crud.get_note_by_id(db, note_id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this summary")
    summary = crud.get_summary(db, note_id=note_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary
