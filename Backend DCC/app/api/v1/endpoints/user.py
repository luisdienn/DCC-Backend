from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserResponseSchema
from app.repository.user_repository import UserRepository

router = APIRouter()

@router.get("/me", response_model=UserResponseSchema)
async def get_current_user(email: str):
    user = await UserRepository.get_user_by_email(email)
    if not user:
        return {"error": "Usuario no encontrado"}
    return user
