from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum
from typing import Optional

class ChatType(str, Enum):
    personal = "personal"
    group = "group"

class ChatCreate(BaseModel):
    name: str
    chat_type: ChatType

class ChatResponse(BaseModel):
    chat_id: Optional[UUID]
    account_id: str
    chat_type: ChatType
    name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    active: Optional[bool]

    class Config:
        orm_mode = True
