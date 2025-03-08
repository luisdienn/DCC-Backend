from pydantic import BaseModel
from typing import List
from datetime import datetime

class ReviewModel(BaseModel):
    estrellas: int
    etiquetas: List[str]
    comentario: str
    id_profesor: str
    fecha_creacion: datetime = datetime.utcnow()