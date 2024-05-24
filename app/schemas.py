from pydantic import BaseModel, conint
from typing import List, Optional
from uuid import UUID

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    content: Optional[str] = None

class Note(NoteBase):
    id: UUID
    owner_id: UUID
    feedbacks: List['Feedback'] = []
    summaries: List['Summary'] = []

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    notes: List[Note] = []

    class Config:
        from_attributes = True

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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
