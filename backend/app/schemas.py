
from pydantic import BaseModel, conint
from typing import Optional
from uuid import UUID
from datetime import datetime


class NoteUpdateFull(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class FeedbackBase(BaseModel):
    comment: Optional[str] = None
    rating: Optional[conint(ge=0, le=5)] = None

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: UUID
    note_id: UUID
    author_id: UUID

    class Config:
        from_attributes = True

class SummaryBase(BaseModel):
    content: str

class SummaryCreate(SummaryBase):
    pass

class Summary(SummaryBase):
    id: UUID
    note_id: UUID
    author_id: UUID

    class Config:
        from_attributes = True

class Note(NoteBase):
    id: UUID
    owner_id: UUID
    created_at: datetime
    feedback: Optional['Feedback'] = None
    summary: Optional['Summary'] = None

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    notes: list[Note] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

