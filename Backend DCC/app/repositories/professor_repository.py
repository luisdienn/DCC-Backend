from motor.motor_asyncio import AsyncIOMotorCollection
from app.schemas.professor_schema import ProfessorCreateSchema
from bson import ObjectId

class ProfessorRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection  # Inyección de dependencia

    async def get_professors_by_name_or_lastname(self, name: str):
        palabras = name.split()  # Divide "Juan Pérez" en ["Juan", "Pérez"]

        criterios = []
        for palabra in palabras:
            criterios.append({"nombre": {"$regex": palabra, "$options": "i"}})
            criterios.append({"apellidos": {"$regex": palabra, "$options": "i"}})

        cursor = self.collection.find({
            "$or": criterios  # Busca coincidencias en nombre o apellido
        })

        return await cursor.to_list(length=10)

    async def get_all_professors(self):
        cursor = self.collection.find({})  # Obtener todos los documentos
        professors = await cursor.to_list(length=100)  # Limita a 100 resultados por optimización
        return [{**professor, "id": str(professor["_id"])} for professor in professors]  # Convertir _id a str
