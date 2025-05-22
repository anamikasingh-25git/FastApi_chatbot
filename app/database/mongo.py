from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
mongo_db = mongo_client.chatdb  # You can replace "chatdb" with your actual DB name

async def get_mongo_client():
    return mongo_client
