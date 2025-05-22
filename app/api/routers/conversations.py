from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.database.session import get_db
from app.schemas.conversations import ConversationCreate, ConversationOut
from app.models.chat import Conversation
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/conversation", response_model=ConversationOut)
def create_conversation(
    payload: ConversationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    conversation = Conversation(
        chat_id=payload.chat_id,
        account_id=payload.account_id,
        name=payload.name,
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation
