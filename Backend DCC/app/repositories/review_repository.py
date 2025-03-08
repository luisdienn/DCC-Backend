from motor.motor_asyncio import AsyncIOMotorCollection
from app.schemas.review_schema import ReviewCreateSchema
from bson import ObjectId

class ReviewRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection  # Inyección de dependencia

    # Create
    async def create_review(self, review: ReviewCreateSchema):
        result = await self.collection.insert_one(review.dict())
        return str("La review ha sido creada con éxito. ID: " + str(result.inserted_id))
    
    # Read
    async def get_all_reviews(self):
        cursor = self.collection.find({})  # Obtener todos los documentos
        reviews = await cursor.to_list(length=100)  # Limita a 100 resultados por optimización
        return [{**review, "id": str(review["_id"])} for review in reviews]  # Convertir _id a str
        
    #Update
    async def update_review(self, review_id: str, review: ReviewCreateSchema):
        await self.collection.update_one({"_id": ObjectId(review_id)}, {"$set": review.dict()})
        return "La review ha sido actualizada con éxito."
        
    #Delete
    async def delete_review(self, review_id: str):
        await self.collection.delete_one({"_id": ObjectId(review_id)})
        return "La review ha sido eliminada con éxito."
