from pydantic import BaseModel, EmailStr

class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str  # La API recibe la contraseña en texto plano

class UserResponseSchema(BaseModel):
    id: str
    name: str
    email: EmailStr  # No devolvemos la contraseña
