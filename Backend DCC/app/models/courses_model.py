from pydantic import BaseModel

class CoursesModel(BaseModel):
    id: str
    nombre: str