from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schema import UserResponseSchema, UserCreateSchema
from app.services.user_service import UserService
from app.core.database import users_collection
from app.repositories.user_repository import UserRepository
from datetime import datetime

router = APIRouter()

# Crear instancias de repositorio y servicio
user_repo = UserRepository(users_collection)
user_service = UserService(user_repo)

# Buscar usuarios por nombre o apellidos
@router.get("/search/{name}", response_model=list[UserResponseSchema])
async def search_users(name: str, service: UserService = Depends(lambda: user_service)):
    users = await service.search_users(name)
    if not users:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios")
    return users

# Obtener usuario actual por correo
@router.get("/me", response_model=UserResponseSchema)
async def get_current_user(email: str, service: UserService = Depends(lambda: user_service)):
    user = await service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# Crear un usuario
@router.post("/create", response_model=str)
async def create_user(user: UserCreateSchema, service: UserService = Depends(lambda: user_service)):
    # Verificar si el usuario ya existe por su correo
    existing_user = await service.get_user_by_email(user.correo)
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    user_dict = user.dict()
    user_dict["fecha_creacion"] = datetime.utcnow()
    user_dict["rol"] = user_dict.get("rol", "estudiante")

    result = await service.create_user(user_dict)
    return f"Usuario creado con éxito. ID: {result}"


# Obtener un usuario por ID
@router.get("/getById/{user_id}", response_model=UserResponseSchema)
async def get_user_by_id(user_id: str, service: UserService = Depends(lambda: user_service)):
    user = await service.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user

# Obtener todos los usuarios
@router.get("/getAll", response_model=list[UserResponseSchema])
async def get_all_users(service: UserService = Depends(lambda: user_service)):
    users = await service.get_all_users()

    formatted_users = [
        {
            "id": str(user["_id"]),
            "correo": user["correo"],
            "nombre": user["nombre"],
            "apellidos": user["apellidos"],
            "fecha_creacion": user.get("fecha_creacion", datetime.utcnow()),
            "rol": user.get("rol", "estudiante")
        }
        for user in users
    ]

    return formatted_users

# Actualizar un usuario
@router.put("/update/{user_id}", response_model=str)
async def update_user(user_id: str, user: UserCreateSchema, service: UserService = Depends(lambda: user_service)):
    user_dict = user.dict()

    result = await service.update_user(user_id, user_dict)

    return f"Usuario con ID {user_id} actualizado correctamente."

# Eliminar un usuario
@router.delete("/delete/{user_id}", response_model=str)
async def delete_user(user_id: str, service: UserService = Depends(lambda: user_service)):
    return await service.delete_user(user_id)
