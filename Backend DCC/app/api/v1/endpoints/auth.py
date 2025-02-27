from fastapi import APIRouter, Depends
from app.services.auth_service import AuthService

router = APIRouter()

@router.get("/auth/google")
async def login_google(access_token: str):
    user = await AuthService.authenticate_with_google(access_token)
    if not user:
        return {"error": "Autenticación fallida"}
    return user
