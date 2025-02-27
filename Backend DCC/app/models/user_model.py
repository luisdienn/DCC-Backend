from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime

class UserModel(BaseModel):
    id: Optional[str] = None
    nombre: str
    correo: EmailStr
    imagen_perfil: Optional[HttpUrl]
    fecha_creacion: datetime = datetime.utcnow()
    rol: Optional[str] = "estudiante"

    class Config:
        from_attributes = True
