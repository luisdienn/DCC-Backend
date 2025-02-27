from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreateSchema

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository  # Inyectamos el repositorio

    async def create_user(self, user_data: UserCreateSchema):
        return await self.repository.create_user(user_data)

    async def get_user_by_email(self, email: str):
        return await self.repository.get_user_by_email(email)
