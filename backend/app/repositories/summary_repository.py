from sqlalchemy.orm import Session
from uuid import UUID
from app.models import Summary
from app.schemas import SummaryCreate

class SummaryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_summary(self, summary: SummaryCreate, note_id: UUID, user_id: UUID):
        db_summary = Summary(**summary.dict(), note_id=note_id, author_id=user_id)
        self.db.add(db_summary)
        self.db.commit()
        self.db.refresh(db_summary)
        return db_summary

    def get_summary(self, note_id: UUID):
        return self.db.query(Summary).filter(Summary.note_id == note_id).first()

    def update_summary(self, summary_id: UUID, summary_update: SummaryCreate):
        summary = self.db.query(Summary).filter(Summary.id == summary_id).first()
        if summary:
            summary.content = summary_update.content
            self.db.commit()
            self.db.refresh(summary)
        return summary
