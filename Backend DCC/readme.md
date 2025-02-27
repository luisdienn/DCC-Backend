# 📌 Guía de Desarrollo - FastAPI + Google OAuth2 + MongoDB

Este documento explica el flujo de trabajo y el orden en el que se deben construir las funcionalidades en la API, siguiendo **Clean Architecture**.

---

## 🔄 Flujo de Trabajo Paso a Paso

### 1️⃣ Definir el Modelo de Datos en `models/`
📌 **Objetivo:** Definir la estructura del documento en **MongoDB** usando **Pydantic**.  
📌 **Ubicación:** `app/models/`  
📌 **Ejemplo:** `app/models/user_model.py`

```python
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime

class UserModel(BaseModel):
    id: Optional[str] = None
    nombre: str
    correo: EmailStr
    imagen_perfil: Optional[HttpUrl]
    fecha_creacion: datetime = datetime.utcnow()
    rol: Optional[str] = "estudiante"

    class Config:
        from_attributes = True 
```

### 2️⃣ Definir los Esquemas de Validación en `schemas/`
📌 **Objetivo:** Especificar qué datos espera la API y qué datos devuelve.  
📌 **Ubicación:** `app/schemas/`  
📌 **Ejemplo:** `app/schemas/user_schema.py`

```python
    from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime

class UserCreateSchema(BaseModel):
    nombre: str
    correo: EmailStr
    imagen_perfil: Optional[HttpUrl]

class UserResponseSchema(BaseModel):
    id: str
    nombre: str
    correo: EmailStr
    imagen_perfil: Optional[HttpUrl]
    fecha_creacion: datetime
    rol: Optional[str] = "estudiante"
```

### 3️⃣ Configurar la Base de Datos en `core/database.py`
📌 **Objetivo:** Configurar la Base de Datos en `core/database.py`.  
📌 **Ubicación:** `app/core/`  
📌 **Ejemplo:** `app/core/database.py`

```python
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
database = client[settings.DATABASE_NAME]

# Definir la colección de usuarios
users_collection = database["students"]
```

### 4️⃣ Crear el Repositorio en `repository/`
📌 **Objetivo:** Gestionar la comunicación entre la API y la base de datos.  
📌 **Ubicación:** `app/repository/`  
📌 **Ejemplo:** `app/repository/user_repository.py`

```python
from app.core.database import users_collection
from datetime import datetime
from bson import ObjectId

class UserRepository:
    @staticmethod
    async def create_user(user_data):
        user_dict = user_data.dict()
        user_dict["fecha_creacion"] = datetime.utcnow()
        user_dict["rol"] = "estudiante"
        
        result = await users_collection.insert_one(user_dict)
        return str(result.inserted_id)

    @staticmethod
    async def get_user_by_email(email: str):
        return await users_collection.find_one({"correo": email})
```

### 5️⃣ Definir la Lógica de Negocio en `services/`
📌 **Objetivo:** Manejar la lógica de autenticación y reglas de negocio.
📌 **Ubicación:** `app/services/`  
📌 **Ejemplo:** `app/services/auth_service.py`

```python
import httpx
from app.repository.user_repository import UserRepository

class AuthService:
    @staticmethod
    async def get_google_user(access_token: str):
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
        return resp.json() if resp.status_code == 200 else None

    @staticmethod
    async def authenticate_with_google(access_token: str):
        user_data = await AuthService.get_google_user(access_token)
        if not user_data:
            return None

        existing_user = await UserRepository.get_user_by_email(user_data["email"])
        if not existing_user:
            new_user = {
                "nombre": user_data["name"],
                "correo": user_data["email"],
                "imagen_perfil": user_data.get("picture"),
            }
            user_id = await UserRepository.create_user(new_user)
            return {"id": user_id, **new_user}

        return existing_user
```

### 6️⃣ Crear los Endpoints en `api/v1/endpoints/`
📌 **Objetivo:** Exponer los servicios mediante HTTP con FastAPI.
📌 **Ubicación:** `app/api/v1/endpoints/`  
📌 **Ejemplo:** `app/api/v1/endpoints/auth.py`

```python
from fastapi import APIRouter, Depends
from app.services.auth_service import AuthService

router = APIRouter()

@router.get("/google-login")
async def login_google(access_token: str):
    user = await AuthService.authenticate_with_google(access_token)
    if not user:
        return {"error": "Autenticación fallida"}
    return user
```

### 7️⃣ Registrar las Rutas en `api/v1/routes.py`
📌 **Objetivo:** Centralizar los endpoints en un solo archivo.
📌 **Ubicación:** `app/api/v1/routes.py`  
📌 **Ejemplo:** `app/api/v1/routes.py`

```python
from fastapi import APIRouter
from app.api.v1.endpoints import auth, user

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(user.router, prefix="/users", tags=["Users"])
```

### 🛠 Cómo Probar la API

## 1️⃣ Instalar dependencias:
```bash
pip install -r requirements.txt
```

## 2️⃣ Crear y activar un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
venv\Scripts\activate
```

## 3️⃣ Configurar el archivo .env
Debes crear un archivo `.env` en la raíz del proyecto con las variables necesarias, por ejemplo:

#### MongoDB
MONGO_URI=***   
DATABASE_NAME=***

#### Google OAuth 2.0
GOOGLE_CLIENT_ID=tu_google_client_id  
GOOGLE_CLIENT_SECRET=tu_google_client_secret  
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback

## 4️⃣ Ejecutar MongoDB local o en la nube.

## 5️⃣ Iniciar la API:
```bash
python -m uvicorn app.main:app --reload
```

## 6️⃣ Acceder a la documentación de la API:

Visita la documentación de **Swagger UI** en: `http://127.0.0.1:8000/docs`