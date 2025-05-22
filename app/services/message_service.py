from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from uuid import uuid4

async def add_message(mongo_client: AsyncIOMotorClient, chat_id: str, question: str, response: str):
    collection = mongo_client.chatdb.chat_content
    response_id = str(uuid4())
    message = {
        "question": question,
        "response": response,
        "response_id": response_id,
        "timestamp": datetime.utcnow().isoformat(),
        "branches": []
    }
    existing = await collection.find_one({"chat_id": chat_id})
    if existing:
        await collection.update_one({"chat_id": chat_id}, {"$push": {"qa_pairs": message}})
    else:
        await collection.insert_one({"chat_id": chat_id, "qa_pairs": [message]})
    return message