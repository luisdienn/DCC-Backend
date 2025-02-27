from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schema import UserResponseSchema
from app.services.user_service import UserService
from app.core.database import users_collection
from app.repositories.user_repository import UserRepository

router = APIRouter()

# Crear instancias de repositorio y servicio
user_repo = UserRepository(users_collection)
user_service = UserService(user_repo)

@router.get("/me", response_model=UserResponseSchema)
async def get_current_user(email: str, service: UserService = Depends(lambda: user_service)):
    user = await service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

