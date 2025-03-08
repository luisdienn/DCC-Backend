from motor.motor_asyncio import AsyncIOMotorCollection
from app.schemas.course_schema import CourseCreateSchema
from bson import ObjectId

class CourseRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection  # Inyección de dependencia


    #CREATE
    async def create_course(self, course: CourseCreateSchema):
        result = await self.collection.insert_one(course.dict())
        return str("El curso ha sido creado con éxito. ID: " + str(result.inserted_id))
    #READ
    async def get_course_by_id(self, course_id: str):
        course = await self.collection.find_one({"_id": ObjectId(course_id)})
        return {**course, "id": str(course["_id"])}
    
    async def get_all_courses(self):
        cursor = self.collection.find({})  # Obtener todos los documentos
        courses = await cursor.to_list(length=100)  # Limita a 100 resultados por optimización
        return [{**course, "id": str(course["_id"])} for course in courses]  # Convertir _id a str
    
    #UPDATE
    async def update_course(self, course_id: str, course: CourseCreateSchema):
        await self.collection.update_one({"_id": ObjectId(course_id)}, {"$set": course.dict()})
        return "El curso ha sido actualizado con éxito."\
        
    #DELETE
    async def delete_course(self, course_id: str):
        await self.collection.delete_one({"_id": ObjectId(course_id)})
        return "El curso ha sido eliminado con éxito."
