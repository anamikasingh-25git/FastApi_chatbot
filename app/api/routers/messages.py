from fastapi import APIRouter, Depends, HTTPException
from app.schemas.message import MessageCreate, MessageOut
from app.services.message_service import add_message
from app.database.mongo import get_mongo_client

router = APIRouter()

@router.post("/add-message", response_model=MessageOut)
async def add_message_route(
    message: MessageCreate,
    mongo_client = Depends(get_mongo_client)
):
    return await add_message(mongo_client, str(message.chat_id), message.question, message.response)

@router.get("/all-messages")
async def get_all_messages(mongo_client = Depends(get_mongo_client)):
    collection = mongo_client.chatdb.chat_content
    messages = await collection.find().to_list(100)
    return messages