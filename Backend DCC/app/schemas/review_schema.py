from pydantic import BaseModel
from typing import List
from datetime import datetime

class ReviewCreateSchema(BaseModel):
    estrellas: int
    etiquetas: List[str]
    comentario: str
    id_profesor: str

class ReviewResponseSchema(BaseModel):
    estrellas: int
    etiquetas: List[str]
    comentario: str
    id_profesor: str
    fecha_creacion: datetime 
