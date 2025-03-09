from pydantic import BaseModel
from typing import List
from datetime import datetime

class CourseCreateSchema(BaseModel):
    nombre: str

class CourseResponseSchema(BaseModel):
    id : str
    nombre: str
