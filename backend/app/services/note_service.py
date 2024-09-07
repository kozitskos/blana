from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import NoteCreate
from app.repositories.note_repository import NoteRepository

from fastapi import HTTPException
from uuid import UUID
from sqlalchemy.orm import Session
from app.repositories.note_repository import NoteRepository
from app.schemas import NoteCreate, NoteUpdate, NoteUpdateFull

class NoteService:
    def __init__(self, db: Session):
        self.note_repository = NoteRepository(db)

    def get_notes(self, user_id: UUID):
        return self.note_repository.get_notes(user_id)

    def create_user_note(self, note: NoteCreate, user_id: UUID):
        return self.note_repository.create_user_note(note, user_id)

    def get_note_by_id(self, note_id: UUID, user_id: UUID):
        note = self.note_repository.get_note_by_id(note_id)
        if not note or note.owner_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this note")
        return note

    def update_note(self, note_id: UUID, note_update: NoteUpdateFull, user_id: UUID):
        # Ensure the user owns the note
        note = self.get_note_by_id(note_id, user_id)
        
        # Replace the entire note object with the new data
        note.title = note_update.title
        note.content = note_update.content
        
        # Save changes to the database
        return self.note_repository.update_note_content(note)

    def delete_note(self, note_id: UUID, user_id: UUID):
        note = self.get_note_by_id(note_id, user_id)  # Ensure the user owns the note
        self.note_repository.delete_note(note_id)


    def patch_note_content(self, note_id: UUID, note_update: NoteUpdate, user_id: UUID):
    # Ensure the user owns the note
        note = self.get_note_by_id(note_id, user_id)

     

        # Update only the fields that are provided
        if note_update.title is not None:
            note.title = note_update.title
        if note_update.content is not None:
            note.content = note_update.content
        # Print the note object to verify before passing it to the repository
    
            # Save changes to the database
        return self.note_repository.update_note_content(note)

    # def patch_note_content(self, note_id: UUID, content: str, user_id: UUID):
    #     note = self.get_note_by_id(note_id, user_id)  # Ensure the user owns the note
    #     if content:
    #         return self.note_repository.update_note_content(note_id, content)
    #     return note
