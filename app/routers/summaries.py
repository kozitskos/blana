from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List


from .. import schemas, crud
from ..database import get_db
from ..deps import get_current_user

router = APIRouter()

@router.post("/{note_id}/summaries/", response_model=schemas.Summary)
def create_summary_for_note(
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

@router.get("/{note_id}/summaries/", response_model=List[schemas.Summary])
def read_summaries(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    note = crud.get_note_by_id(db, note_id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access summaries for this note")
    return crud.get_summaries(db=db, note_id=note_id)
