from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime

class UserCreateSchema(BaseModel):
    nombre: str
    correo: EmailStr

class UserResponseSchema(BaseModel):
    id: str
    nombre: str
    correo: EmailStr
    imagen_perfil: Optional[HttpUrl]
    fecha_creacion: datetime
    rol: Optional[str] = "estudiante"
