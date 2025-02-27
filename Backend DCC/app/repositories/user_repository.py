from motor.motor_asyncio import AsyncIOMotorCollection
from app.schemas.user_schema import UserCreateSchema
from datetime import datetime
from bson import ObjectId

class UserRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection  # Inyección de dependencia

    async def create_user(self, user_data: UserCreateSchema) -> str:
        user_dict = user_data.dict()
        user_dict["fecha_creacion"] = datetime.utcnow()
        user_dict["rol"] = "estudiante"

        result = await self.collection.insert_one(user_dict)
        return str(result.inserted_id)

    async def get_user_by_email(self, email: str):
        user = await self.collection.find_one({"correo": email})
        if user:
            user["id"] = str(user["_id"])
            del user["_id"]
        return user