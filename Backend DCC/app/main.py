from fastapi import FastAPI
from app.api.v1.routes import router as api_router
from app.core.database import client

app = FastAPI(title="FastAPI + MongoDB + Google OAuth2 API")

app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup():
    print("Conectado a MongoDB...")

@app.on_event("shutdown")
async def shutdown():
    client.close()
    print("Desconectado de MongoDB.")
