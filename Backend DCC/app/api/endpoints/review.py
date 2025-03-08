from fastapi import APIRouter, Depends, HTTPException
from app.schemas.review_schema import ReviewResponseSchema
from app.services.review_service import ReviewService
from app.core.database import reviews_collection
from app.repositories.review_repository import ReviewRepository

router = APIRouter()

# Crear instancias de repositorio y servicio
review_repo = ReviewRepository(reviews_collection)
review_service = ReviewService(review_repo)

#Create
@router.post("/create", response_model=str)
async def create_review(review: ReviewResponseSchema, service: ReviewService = Depends(lambda: review_service)):
    return await service.create_review(review)
              
#Read
@router.get("/", response_model=list[ReviewResponseSchema])
async def get_all_reviews(service: ReviewService = Depends(lambda: review_service)):
    return await service.get_all_reviews()

#Update
@router.put("/{review_id}", response_model=str)
async def update_review(review_id: str, review: ReviewResponseSchema, service: ReviewService = Depends(lambda: review_service)):
    return await service.update_review(review_id, review)

#Delete
@router.delete("/{review_id}", response_model=str)
async def delete_review(review_id: str, service: ReviewService = Depends(lambda: review_service)):
    return await service.update_review(review_id)