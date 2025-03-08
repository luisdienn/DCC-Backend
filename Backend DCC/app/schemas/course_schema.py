from pydantic import BaseModel
from typing import List
from datetime import datetime

class CourseCreateSchema(BaseModel):
    nombre: str

class CourseResponseSchema(BaseModel):
    nombre: str
