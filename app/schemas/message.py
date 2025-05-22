from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class MessageCreate(BaseModel):
    chat_id: UUID
    question: str
    response: str

class MessageOut(BaseModel):
    response_id: str
    question: str
    response: str
    timestamp: datetime
    branches: list[str] = []