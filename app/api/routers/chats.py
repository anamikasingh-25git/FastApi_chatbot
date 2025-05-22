from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.chat import ChatCreate, ChatResponse
from app.services.chat_service import create_chat as service_create_chat
from app.dependencies import get_current_user
from app.models.chat import Chat
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter()

@router.post("/create-chat", response_model=ChatResponse)
async def create_chat(
    chat: ChatCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    account_id = current_user.get("user_id")
    if not account_id:
        raise HTTPException(status_code=400, detail="Invalid user")
    new_chat = await service_create_chat(db, account_id, chat)
    return new_chat


@router.get("/get-chat", response_model=list[ChatResponse])
def get_chats(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Chat).filter(Chat.account_id == current_user["user_id"]).all()

@router.put("/update-chat/{chat_id}", response_model=ChatResponse)
def update_chat(chat_id: UUID, chat: ChatCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_chat = db.query(Chat).filter(Chat.chat_id == chat_id, Chat.account_id == current_user["user_id"]).first()
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    db_chat.name = chat.name
    db_chat.chat_type = chat.chat_type
    db.commit()
    db.refresh(db_chat)
    return db_chat

@router.delete("/delete-chat/{chat_id}")
def delete_chat(chat_id: UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.chat_id == chat_id, Chat.account_id == current_user["user_id"]).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    db.delete(chat)
    db.commit()
    return {"msg": "Chat deleted"}