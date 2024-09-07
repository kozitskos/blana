from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from app.models import Note
from app.schemas import NoteCreate

class NoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_notes(self, user_id: UUID):
        return self.db.query(Note).filter(Note.owner_id == user_id).all()


    def create_user_note(self, note: NoteCreate, user_id: UUID):
        db_note = Note(
            id=uuid4(),  # Generate a new UUID for the note (if required)
            title=note.title,
            content=note.content,
            owner_id=user_id  # Pass the user ID
        )
        self.db.add(db_note)
        self.db.commit()
        self.db.refresh(db_note)
        return db_note

    def get_note_by_id(self, note_id: UUID):
        return self.db.query(Note).filter(Note.id == note_id).first()

    # def update_note_content(self, note_id: UUID, content: str):
    #     note = self.db.query(Note).filter(Note.id == note_id).first()
    #     if note:
    #         note.content = content
    #         self.db.commit()
    #         self.db.refresh(note)
    #     return note
    
    def update_note_content(self, note):
        try:

            self.db.commit()
            self.db.refresh(note)
            return note
        except StaleDataError:
            # In case the object is stale or cannot be refreshed, rollback the session
            self.db.rollback()
            raise ValueError("Failed to update note, possibly due to stale data or concurrency issues.")
        except Exception as e:
            # Rollback if any other exception occurs
            self.db.rollback()
            raise ValueError(f"An error occurred during note update: {e}")

    # def patch_note_content(self, note_id: UUID, updated_data: dict):
    #     note = self.get_note_by_id(note_id)
    #     if note:
    #         if 'title' in updated_data:
    #             note.title = updated_data['title']
    #         if 'content' in updated_data:
    #             note.content = updated_data['content']
                
    #         self.db.commit()
    #         self.db.refresh(note)
    #         return note
            
    def delete_note(self, note_id: UUID):
        note = self.get_note_by_id(note_id)
        if note:
            self.db.delete(note)
            self.db.commit()
