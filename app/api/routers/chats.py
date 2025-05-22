from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.chat import ChatCreate, ChatResponse
from app.services.chat_service import create_chat as service_create_chat
from app.dependencies import get_current_user
from app.models.chat import Chat
from sqlalchemy.orm import Session
from sqlalchemy import select

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
async def get_chats(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    stmt = select(Chat).where(Chat.account_id == current_user["user_id"])
    result = await db.execute(stmt)
    chats = result.scalars().all()
    return chats


@router.put("/update-chat/{chat_id}", response_model=ChatResponse)
async def update_chat(chat_id: UUID, chat: ChatCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    stmt = select(Chat).where(Chat.chat_id == chat_id, Chat.account_id == current_user["user_id"])
    result = await db.execute(stmt)
    db_chat = result.scalar_one_or_none()
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    db_chat.name = chat.name
    db_chat.chat_type = chat.chat_type
    await db.commit()
    await db.refresh(db_chat)
    return db_chat



@router.delete("/delete-chat/{chat_id}")
async def delete_chat(chat_id: UUID, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    stmt = select(Chat).where(Chat.chat_id == chat_id, Chat.account_id == current_user["user_id"])
    result = await db.execute(stmt)
    chat = result.scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    await db.delete(chat)
    await db.commit()
    return {"msg": "Chat deleted"}