from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


# --------- ROUTES --------- #
from app.api.routes import router as api_router
from app.api.endpoints.auth import auth_router  # Importamos la ruta de autenticación

# --------- REPOSITORIES --------- #
from app.repositories.user_repository import UserRepository
from app.repositories.professor_repository import ProfessorRepository
from app.repositories.review_repository import ReviewRepository
from app.repositories.course_repository import CourseRepository

# --------- SERVICES --------- #
from app.services.user_service import UserService
from app.services.professor_service import ProfessorService
from app.services.review_service import ReviewService
from app.services.course_service import CourseService

# --------- COLLECTIONS --------- #
from app.core.database import client, users_collection, professors_collection, reviews_collection, courses_collection

app = FastAPI(title="FastAPI + MongoDB + Google OAuth2 API")

# 📌 Inyección de dependencias Repositories
user_repo = UserRepository(users_collection)
professor_repo = ProfessorRepository(professors_collection)
review_repo = ReviewRepository(reviews_collection)
course_repo = CourseRepository(courses_collection)

# 📌 Inyección de dependencias Services
user_service = UserService(user_repo)
professor_service = ProfessorService(professor_repo)
review_service = ReviewService(review_repo)
course_service = CourseService(course_repo)

# 📌 Middleware de CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",                     # Desarrollo local
        "https://dcc-frontend-eight.vercel.app"      # Producción en Vercel
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 📌 Incluir las rutas
app.include_router(api_router, prefix="/api")
app.include_router(auth_router, prefix="/auth") 

@app.on_event("startup")
async def startup():
    print("Conectado a MongoDB...")
    print("Servidor corriendo en http://127.0.0.1:8080")

@app.on_event("shutdown")
async def shutdown():
    client.close()
    print("Desconectado de MongoDB.")
