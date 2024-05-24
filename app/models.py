import uuid
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    notes = relationship("Note", back_populates="owner")
    feedbacks = relationship("Feedback", back_populates="author")
    summaries = relationship("Summary", back_populates="author")

class Note(Base):
    __tablename__ = 'notes'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    owner = relationship("User", back_populates="notes")
    feedbacks = relationship("Feedback", back_populates="note")
    summaries = relationship("Summary", back_populates="note")

class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    comment = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)
    note_id = Column(UUID(as_uuid=True), ForeignKey('notes.id'))
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    note = relationship("Note", back_populates="feedbacks")
    author = relationship("User", back_populates="feedbacks")

class Summary(Base):
    __tablename__ = 'summaries'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    content = Column(String)
    note_id = Column(UUID(as_uuid=True), ForeignKey('notes.id'))
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    note = relationship("Note", back_populates="summaries")
    author = relationship("User", back_populates="summaries")
