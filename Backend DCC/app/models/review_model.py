from pydantic import BaseModel,Field
from typing import List
from datetime import datetime

class ReviewModel(BaseModel):
    estrellas: int
    etiquetas: List[str]
    comentario: str
    id_profesor: str
    materia: str
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
