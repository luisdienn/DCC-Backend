from app.repositories.review_repository import ReviewRepository
from app.models.review_model import ReviewModel

class ReviewService:
    def __init__(self, repository: ReviewRepository):
        self.repository = repository  # Inyectamos el repositorio

    #create
    async def create_review(self, review: ReviewModel):
        return await self.repository.create_review(review)
    
    #read
    async def get_all_reviews(self):
        return await self.repository.get_all_reviews()
    
    async def get_all_reviews_by_professor_id(self):
        return await self.repository.get_all_reviews_by_professor_id
    
    async def get_all_reviews_by_professor_id(self, id_profesor: str):  # Se añade el argumento
        return await self.repository.get_all_reviews_by_professor_id(id_profesor) 
    
    #update
    async def update_review(self, review: ReviewModel):
        return await self.repository.update_review(review)

    #delete
    async def delete_review(self, review_id: str):
        return await self.repository.delete_review(review_id)
