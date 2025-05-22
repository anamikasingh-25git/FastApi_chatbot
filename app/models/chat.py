from sqlalchemy import Column, String, DateTime, Boolean, Enum as SqlEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database.base import Base
import enum
from uuid import uuid4


class ChatType(str, enum.Enum):
    personal = "personal"
    group = "group"

class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    account_id = Column(String, nullable=False)
    chat_type = Column(SqlEnum(ChatType), default=ChatType.personal)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = Column(Boolean, default=True)
    conversations = relationship("Conversation", back_populates="chat")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.chat_id"), nullable=False)
    account_id = Column(String, nullable=False)
    name = Column(String)
    deleted = Column(Boolean, default=False)

    chat = relationship("Chat", back_populates="conversations")