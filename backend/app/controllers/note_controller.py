from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.schemas import NoteCreate, Note, NoteUpdate, NoteUpdateFull
from app.services.note_service import NoteService
from app.deps import get_db, get_current_user
from app.schemas import User

router = APIRouter()

@router.post("/", response_model=Note)
def create_note_for_user(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return NoteService(db).create_user_note(note, current_user.id)

@router.get("/", response_model=List[Note])
def read_notes(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return NoteService(db).get_notes(current_user.id)

# New get a specific note by ID
@router.get("/{note_id}", response_model=Note)
def read_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = NoteService(db).get_note_by_id(note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=Note)
def update_note(
    note_id: UUID,
    note_update: NoteUpdateFull,  # Expecting a complete object
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):  
    print(note_update)
    return NoteService(db).update_note(note_id, note_update, current_user.id)

# New delete note endpoint
@router.delete("/{note_id}", response_model=None)
def delete_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    NoteService(db).delete_note(note_id, current_user.id)
    return {"message": "Note deleted successfully"}


@router.patch("/{note_id}", response_model=Note)
def patch_note(
    note_id: UUID,
    note_update: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return NoteService(db).patch_note_content(note_id, note_update, current_user.id)