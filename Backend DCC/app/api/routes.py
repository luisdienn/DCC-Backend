from fastapi import APIRouter
from app.api.endpoints import user, professor

router = APIRouter()
router.include_router(user.router, prefix="/users", tags=["Users"])
router.include_router(professor.router, prefix="/professors", tags=["Professors"])
