from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Conexión a MongoDB
client = AsyncIOMotorClient(settings.MONGO_URI)
database = client[settings.DATABASE_NAME]

# Definimos las colecciones
users_collection = database["users"]