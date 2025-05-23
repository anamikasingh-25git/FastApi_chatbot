from fastapi import APIRouter, Depends, HTTPException
from app.schemas.message import MessageCreate, MessageOut
from app.services.message_service import add_message
from app.database.mongo import get_mongo_client
from bson import ObjectId
router = APIRouter()

# Endpoint to add a message to the database
@router.post("/add-message", response_model=MessageOut)
async def add_message_route(
    message: MessageCreate,  # Pydantic model with message details (chat_id, question, response)
    mongo_client=Depends(get_mongo_client)  # Injected MongoDB client
):
    # Call the service function to insert the message into the appropriate chat
    return await add_message(
        mongo_client,
        str(message.chat_id),  # Ensure chat_id is a string
        message.question,
        message.response
    )

# Utility function to recursively convert ObjectId to string in nested data structures
def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)  # Convert single ObjectId to string
    if isinstance(obj, list):
        return [convert_objectid(i) for i in obj]  # Recursively convert items in list
    if isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}  # Recursively convert values in dict
    return obj  # Return object as-is if no conversion needed

# Endpoint to fetch all messages from the MongoDB collection
@router.get("/all-messages")
async def get_all_messages(mongo_client=Depends(get_mongo_client)):
    # Access the specific collection in the MongoDB database
    collection = mongo_client.chatdb.chat_content
    
    # Fetch up to 100 messages from the collection
    messages = await collection.find().to_list(100)

    # Convert ObjectId fields in messages to strings for JSON serialization
    return [convert_objectid(message) for message in messages]