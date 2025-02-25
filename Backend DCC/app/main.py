from fastapi import FastAPI
from .routes.route import router  # Asegúrate de importar correctamente el router

# Instancia de la aplicación FastAPI
app = FastAPI(
    title="FastAPI + MongoDB API",
    description="API con FastAPI y MongoDB",
    version="1.0.0"
)

# Registramos el router para las rutas de usuario
app.include_router(router, prefix="/api")  # Usamos el prefijo /api