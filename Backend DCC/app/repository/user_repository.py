from app.core.database import users_collection
from app.schemas.user_schema import UserCreateSchema
from datetime import datetime
from bson import ObjectId

class UserRepository:
    @staticmethod
    async def create_user(user_data: UserCreateSchema):
        user_dict = user_data.dict()
        user_dict["fecha_creacion"] = datetime.utcnow()
        user_dict["rol"] = "estudiante"
        
        result = await users_collection.insert_one(user_dict)
        return str(result.inserted_id)

    @staticmethod
    async def get_user_by_email(email: str):
        return await users_collection.find_one({"correo": email})
