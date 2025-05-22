from pydantic import BaseModel
from uuid import UUID
from typing import List

class BranchCreate(BaseModel):
    original_chat_id: UUID
    branch_from_response_id: str
    new_chat_id: UUID

class BranchTree(BaseModel):
    chat_id: UUID
    children: List[UUID] = []

class SetActiveBranch(BaseModel):
    chat_id: UUID
    branch_id: UUID