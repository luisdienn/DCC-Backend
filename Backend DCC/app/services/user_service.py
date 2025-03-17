from app.repositories.user_repository import UserRepository
from app.models.user_model import UserModel
from app.schemas.user_schema import UserCreateSchema

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository  # Inyectamos el repositorio

    # Crear usuario
    async def create_user(self, user_data: dict):
        existing_user = await self.repository.get_user_by_email(user_data["correo"])
        if existing_user:
            return existing_user["id"]  # Devolver ID del usuario existente
        user_obj = UserModel(**user_data)
        return await self.repository.create_user(user_obj)

    # Obtener usuario por ID
    async def get_user_by_id(self, user_id: str):
        return await self.repository.get_user_by_id(user_id)
    
    # Obtener usuario por correo
    async def get_user_by_email(self, email: str):
        return await self.repository.get_user_by_email(email)

    # Obtener todos los usuarios
    async def get_users(self):
        return await self.repository.get_all_users()
    
    # Actualizar usuario
    async def update_user(self, user_id: str, user: UserModel):
        return await self.repository.update_user(user_id, user)
    
    # Eliminar usuario
    async def delete_user(self, user_id: str):
        return await self.repository.delete_user(user_id)
