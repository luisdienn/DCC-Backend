from motor.motor_asyncio import AsyncIOMotorCollection
from app.schemas.user_schema import UserCreateSchema
from datetime import datetime
from bson import ObjectId
import re
from typing import List, Dict

class UserRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection  # Inyección de dependencia

    # Crear usuario (si no existe, lo crea; si existe, usa el existente)
    async def create_user(self, user_data: UserCreateSchema) -> str:
        user_dict = user_data.dict()
        user_dict["fecha_creacion"] = datetime.utcnow()
        user_dict["rol"] = user_dict.get("rol", "estudiante")

        # Verificar si el usuario ya existe por su correo
        existing_user = await self.collection.find_one({"correo": user_dict["correo"]})

        if existing_user:
            return str(existing_user["_id"])  # Devolver el ID del usuario existente

        # Crear el usuario si no existe
        result = await self.collection.insert_one(user_dict)
        return str(result.inserted_id)

    # Obtener usuario por correo
    async def get_user_by_email(self, email: str):
        user = await self.collection.find_one({"correo": email})
        if user:
            user["id"] = str(user["_id"])
            del user["_id"]
        return user

    # Obtener usuario por ID
    async def get_user_by_id(self, user_id: str):
        user = await self.collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            return None

        return {
            "id": str(user["_id"]),
            "correo": user.get("correo", ""),
            "nombre": user.get("nombre", ""),
            "apellidos": user.get("apellidos", ""),
            "fecha_creacion": user.get("fecha_creacion", ""),
            "rol": user.get("rol", "estudiante"),
        }

    # Obtener todos los usuarios
    async def get_all_users(self) -> List[Dict]:
        cursor = self.collection.find({})
        users = await cursor.to_list(length=100)  # Limitar a 100 resultados

        return [
            {
                **user,
                "id": str(user["_id"]),
            }
            for user in users
        ]

    # Buscar usuarios por nombre o apellidos
    async def get_users_by_name_or_lastname(self, name: str) -> List[Dict]:
        palabras = [re.escape(palabra) for palabra in name.strip().split() if palabra]

        if not palabras:
            return []

        criterios = [{"nombre": {"$regex": palabra, "$options": "i"}} for palabra in palabras] + \
                    [{"apellidos": {"$regex": palabra, "$options": "i"}} for palabra in palabras]

        cursor = self.collection.find({"$or": criterios})

        resultados = await cursor.to_list(length=10)  # Limitar a 10 resultados

        usuarios = [
            {
                **user,
                "id": str(user["_id"]),
            }
            for user in resultados
        ]

        return usuarios

    # Actualizar usuario
    async def update_user(self, user_id: str, user_data: UserCreateSchema) -> str:
        user_dict = user_data.dict()

        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": user_dict}
        )

        return "El usuario ha sido actualizado con éxito." + str(result.raw_result)

    # Eliminar usuario
    async def delete_user(self, user_id: str) -> str:
        await self.collection.delete_one({"_id": ObjectId(user_id)})
        return "El usuario ha sido eliminado con éxito."
