from pydantic import BaseModel,EmailStr
from typing import Optional, List
from datetime import datetime

class CoursesModel(BaseModel):
    id: str
    nombre: str

class ProfessorModel(BaseModel):
    id: Optional[str] = None
    correo: EmailStr
    nombre: str
    apellidos: str
    universidad: str = "Cenfotec"
    materias: List[CoursesModel] # Lista de materias
    fecha_creacion: datetime = datetime.utcnow()