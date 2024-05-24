import uuid
from sqlalchemy import Column, String, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    notes = relationship("Note", back_populates="owner")

class Note(Base):
    __tablename__ = 'notes'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    owner = relationship("User", back_populates="notes")
    feedback = relationship("Feedback", uselist=False, back_populates="note", cascade="all, delete-orphan")
    summary = relationship("Summary", uselist=False, back_populates="note", cascade="all, delete-orphan")

class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    comment = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)
    note_id = Column(UUID(as_uuid=True), ForeignKey('notes.id'), unique=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    note = relationship("Note", back_populates="feedback")

class Summary(Base):
    __tablename__ = 'summaries'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    content = Column(Text, nullable=False)
    note_id = Column(UUID(as_uuid=True), ForeignKey('notes.id'), unique=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    note = relationship("Note", back_populates="summary")
