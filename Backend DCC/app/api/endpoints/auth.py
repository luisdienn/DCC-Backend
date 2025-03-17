from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.core.database import users_collection

# Crear instancia del repositorio y servicio
user_repo = UserRepository(users_collection)
user_service = UserService(user_repo)

auth_router = APIRouter()

class GoogleAuthRequest(BaseModel):
    email: str
    name: str

@auth_router.post("/google-login")
async def google_login(auth_data: GoogleAuthRequest, service: UserService = Depends(lambda: user_service)):
    # Verificar si los datos están presentes
    if not auth_data.email or not auth_data.name:
        raise HTTPException(status_code=400, detail="Datos de Google inválidos")

    # Buscar usuario por correo
    user = await service.get_user_by_email(auth_data.email)

    # Si el usuario no existe, crearlo
    if not user:
        user_data = {
            "nombre": auth_data.name,
            "correo": auth_data.email,
            "imagen_perfil": None,  # Opcional: Puedes agregar la imagen si la recibes
            "rol": "estudiante"  # Rol por defecto
        }
        user_id = await service.create_user(user_data)
        return {"message": "Usuario creado con éxito", "id": user_id, "email": auth_data.email}

    return {"message": "Usuario autenticado", "id": user["id"], "email": auth_data.email}
