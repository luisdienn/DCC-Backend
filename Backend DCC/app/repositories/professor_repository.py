from motor.motor_asyncio import AsyncIOMotorCollection
from app.models.professor_model import ProfessorModel
from app.schemas.professor_schema import ProfessorCreateSchema
from bson import ObjectId
import re
from typing import List, Dict

class ProfessorRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection  # Inyección de dependencia



    async def get_professors_by_name_or_lastname(self, name: str) -> List[Dict]:
        palabras = [re.escape(palabra) for palabra in name.strip().split() if palabra]

        if not palabras:
            return []

        criterios = [{"nombre": {"$regex": palabra, "$options": "i"}} for palabra in palabras] + \
                    [{"apellidos": {"$regex": palabra, "$options": "i"}} for palabra in palabras]

        cursor = self.collection.find({"$or": criterios})

        resultados = await cursor.to_list(length=25)

        profesores = [
            {
                **professor,
                "id": str(professor["_id"]),  # Convertir ObjectId a string
            } for professor in resultados
        ]

        return profesores


    

    #Create
    async def create_professor(self, professor: ProfessorCreateSchema):
        professor_dict = professor.dict()
        professor_dict["materias"] = [
        {"id": str(materia["id"]), "nombre": materia["nombre"]}
        for materia in professor_dict["materias"]
        ]

        result = await self.collection.insert_one(professor_dict)
        return str(result.inserted_id)

    #Read

    async def get_professor_by_id(self, professor_id: str):
        professor = await self.collection.find_one({"_id": ObjectId(professor_id)})

        # Si el profesor no existe, devolvemos None
        if not professor:
            return None

        return {
            "id": str(professor["_id"]),
            "correo": professor.get("correo", ""),
            "nombre": professor.get("nombre", ""),
            "apellidos": professor.get("apellidos", ""),
            "universidad": professor.get("universidad", "Cenfotec"),
            "fecha_creacion": professor.get("fecha_creacion", ""),
            "materias": [
                {"id": str(materia["id"]), "nombre": materia["nombre"]}
                for materia in professor.get("materias", []) if isinstance(materia, dict) and "nombre" in materia
            ]
        }
    
    async def get_all_professors(self):
        cursor = self.collection.find({})  # Obtener todos los documentos
        professors = await cursor.to_list(length=100)  # Limitar a 100 resultados

        return [
            {
                **professor, 
                "id": str(professor["_id"]),  # Convertir ObjectId a string
                "materias": [
                    {"id": materia["id"], "nombre": materia["nombre"]}
                    for materia in professor.get("materias", []) if isinstance(materia, dict) and "nombre" in materia
                ]  # Asegurar que las materias sean devueltas correctamente
            } 
            for professor in professors
        ]

    
    #Update
    async def update_professor(self, professor_id: str, professor: ProfessorCreateSchema):

        professor["materias"] = [
        {"id": str(materia["id"]), "nombre": materia["nombre"]}
        for materia in professor["materias"]
        ]



        result = await self.collection.update_one({"_id": ObjectId(professor_id)}, {"$set": professor})
        
        return "El profesor ha sido actualizado con éxito." + str(result.raw_result)
    

    
    #Delete
    async def delete_professor(self, professor_id: str):
        await self.collection.delete_one({"_id": ObjectId(professor_id)})
        return "El profesor ha sido eliminado con éxito."