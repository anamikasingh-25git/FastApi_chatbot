# Import required modules from FastAPI, SQLAlchemy, and local modules
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

# Create a new API router for chat-related endpoints
router = APIRouter()

# Endpoint to create a new chat
@router.post("/create-chat", response_model=ChatResponse)
async def create_chat(
    chat: ChatCreate,  # Chat creation schema from request body
    db: AsyncSession = Depends(get_db),  # Injected async database session
    current_user=Depends(get_current_user)  # Injected current user from dependencies
):
    # Extract the user ID from the current user info
    account_id = current_user.get("user_id")
    if not account_id:
        # Raise error if user ID is missing
        raise HTTPException(status_code=400, detail="Invalid user")
    
    # Call service to create a new chat in the database
    new_chat = await service_create_chat(db, account_id, chat)
    return new_chat

# Endpoint to retrieve all chats for the current user
@router.get("/get-chat", response_model=list[ChatResponse])
async def get_chats(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # SQLAlchemy select query to filter chats by the current user's ID
    stmt = select(Chat).where(Chat.account_id == current_user["user_id"])
    
    # Execute the query
    result = await db.execute(stmt)
    
    # Retrieve all matched chat records
    chats = result.scalars().all()
    return chats

# Endpoint to update an existing chat
@router.put("/update-chat/{chat_id}", response_model=ChatResponse)
async def update_chat(
    chat_id: UUID,  # UUID of the chat to update
    chat: ChatCreate,  # Updated chat data
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Query to find the specific chat belonging to the user
    stmt = select(Chat).where(Chat.chat_id == chat_id, Chat.account_id == current_user["user_id"])
    result = await db.execute(stmt)
    db_chat = result.scalar_one_or_none()

    # Return 404 error if chat not found
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Update the chat's name and type
    db_chat.name = chat.name
    db_chat.chat_type = chat.chat_type

    # Commit changes and refresh the object from the database
    await db.commit()
    await db.refresh(db_chat)
    return db_chat

# Endpoint to delete a chat
@router.delete("/delete-chat/{chat_id}")
async def delete_chat(
    chat_id: UUID,  # UUID of the chat to delete
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Query to find the chat belonging to the user
    stmt = select(Chat).where(Chat.chat_id == chat_id, Chat.account_id == current_user["user_id"])
    result = await db.execute(stmt)
    chat = result.scalar_one_or_none()

    # Raise error if the chat doesn't exist
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Delete the chat from the database
    await db.delete(chat)
    await db.commit()

    # Return a confirmation message
    return {"msg": "Chat deleted"}
