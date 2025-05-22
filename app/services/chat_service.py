from sqlalchemy.ext.asyncio import AsyncSession
from app.models.chat import Chat
from app.schemas.chat import ChatCreate
from uuid import uuid4
from datetime import datetime

async def create_chat(db: AsyncSession, account_id: str, chat: ChatCreate):
    new_chat = Chat(
        chat_id=uuid4(),
        account_id=account_id,
        name=chat.name,
        chat_type=chat.chat_type,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)
    return new_chat