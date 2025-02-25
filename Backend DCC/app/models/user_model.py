from pydantic import BaseModel, EmailStr
from typing import Optional, ClassVar  # Agregamos ClassVar

class UserModel(BaseModel):
    #id: Optional[str] = None
    name: str
    email: EmailStr
    hashed_password: str

    collection_name: ClassVar[str] = "users"  # <-- Corrección

    class Config:
        from_attributes = True  # Cambiar de `orm_mode = True` a `from_attributes = True`

    collection_name = "users"