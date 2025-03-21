from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List
from datetime import datetime
from app.models.courses_model import CoursesModel

class ProfessorCreateSchema(BaseModel):
    correo: EmailStr
    nombre: str
    apellidos: str
    materias: List[CoursesModel]

class ProfessorResponseSchema(BaseModel):
    id: str
    correo: EmailStr
    nombre: str
    apellidos: str
    universidad: str = "Cenfotec"
    materias: List
    fecha_creacion: datetime
