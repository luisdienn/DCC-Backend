from fastapi import APIRouter
from app.api.endpoints import user, professor,review,course

router = APIRouter()
router.include_router(user.router, prefix="/users", tags=["Users"])
router.include_router(professor.router, prefix="/professors", tags=["Professors"])
router.include_router(review.router, prefix="/reviews", tags=["Reviews"])
router.include_router(course.router, prefix="/courses", tags=["Courses"])
