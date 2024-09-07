from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import SummaryCreate
from app.repositories.summary_repository import SummaryRepository

class SummaryService:
    def __init__(self, db: Session):
        self.summary_repository = SummaryRepository(db)

    def create_summary(self, summary: SummaryCreate, note_id: UUID, user_id: UUID):
        return self.summary_repository.create_summary(summary, note_id, user_id)

    def get_summary(self, note_id: UUID):
        return self.summary_repository.get_summary(note_id)

    def update_summary(self, summary_id: UUID, summary_update: SummaryCreate):
        return self.summary_repository.update_summary(summary_id, summary_update)
