from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ConversationCreate(BaseModel):
    chat_id: UUID
    account_id: str
    name: Optional[str] = None

class ConversationOut(BaseModel):
    id: UUID
    chat_id: UUID
    account_id: str
    name: Optional[str]
    deleted: bool

    class Config:
        orm_mode = True
