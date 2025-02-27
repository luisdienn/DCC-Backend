import httpx
from app.core.config import settings
from app.repository.user_repository import UserRepository

class AuthService:
    @staticmethod
    async def get_google_user(access_token: str):
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
        return resp.json() if resp.status_code == 200 else None

    @staticmethod
    async def authenticate_with_google(access_token: str):
        user_data = await AuthService.get_google_user(access_token)
        if not user_data:
            return None

        existing_user = await UserRepository.get_user_by_email(user_data["email"])
        if not existing_user:
            new_user = {
                "nombre": user_data["name"],
                "correo": user_data["email"],
                "imagen_perfil": user_data.get("picture"),
            }
            user_id = await UserRepository.create_user(new_user)
            return {"id": user_id, **new_user}

        return existing_user
