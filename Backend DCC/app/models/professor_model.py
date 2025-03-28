from pydantic import BaseModel,EmailStr
from typing import List
from datetime import datetime
from .courses_model import CoursesModel

class ProfessorModel(BaseModel):
    correo: EmailStr
    nombre: str
    apellidos: str
    universidad: str = "Cenfotec"
    materias: List[CoursesModel] # Lista de materias
    fecha_creacion: datetime = datetime.utcnow()