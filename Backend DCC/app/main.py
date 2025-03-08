from fastapi import FastAPI
from app.api.routes import router as api_router
from app.repositories.user_repository import UserRepository
from app.repositories.professor_repository import ProfessorRepository
from app.services.user_service import UserService
from app.services.professor_service import ProfessorService
from app.core.database import client, users_collection, professors_collection

app = FastAPI(title="FastAPI + MongoDB + Google OAuth2 API")

# Inyección de dependencias Repositories
user_repo = UserRepository(users_collection)
professor_repo = ProfessorRepository(professors_collection)

# Inyección de dependencias Services
user_service = UserService(user_repo)
professor_service = ProfessorService(professor_repo)

app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup():
    print("Conectado a MongoDB...")

@app.on_event("shutdown")
async def shutdown():
    client.close()
    print("Desconectado de MongoDB.")
