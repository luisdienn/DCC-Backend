from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

# Conectamos con MongoDB
client = AsyncIOMotorClient(settings.MONGO_URI)
database = client[settings.DATABASE_NAME] #Folder 