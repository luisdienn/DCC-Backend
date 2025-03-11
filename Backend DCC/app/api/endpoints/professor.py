from fastapi import APIRouter, Depends, HTTPException
from app.schemas.professor_schema import ProfessorResponseSchema, ProfessorCreateSchema
from app.services.professor_service import ProfessorService
from app.core.database import professors_collection
from app.repositories.professor_repository import ProfessorRepository
from datetime import datetime

router = APIRouter()

# Crear instancias de repositorio y servicio
professor_repo = ProfessorRepository(professors_collection)
professor_service = ProfessorService(professor_repo)

@router.get("/search/{name}", response_model=list[ProfessorResponseSchema])
async def search_professors(name: str, service: ProfessorService = Depends(lambda: professor_service)):
    professors = await service.search_professors(name)
    if not professors:
        raise HTTPException(status_code=404, detail="No se encontraron profesores")
    return professors


#Create

@router.post("/create", response_model=str)
async def create_professor(professor: ProfessorCreateSchema, service: ProfessorService = Depends(lambda: professor_service)):
    professor_dict = professor.dict()
    professor_dict["fecha_creacion"] = datetime.utcnow()

    # Asegurar que las materias sean una lista de diccionarios
    if "materias" in professor_dict:
        professor_dict["materias"] = [
            {"id": str(materia["id"]), "nombre": materia["nombre"]}
            for materia in professor_dict["materias"]
            if isinstance(materia, dict) and "id" in materia and "nombre" in materia
        ]

    result = await service.create_professor(professor_dict)
    return f"Profesor creado con éxito. ID: {result}"


              
#Read
@router.get("/getById/{professor_id}", response_model=ProfessorResponseSchema)
async def get_professor(professor_id: str, service: ProfessorService = Depends(lambda: professor_service)):
    professor = await service.get_professor_by_id(professor_id)

    if professor is None:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    
    return professor


@router.get("/getAll", response_model=list[ProfessorResponseSchema])
async def get_all_professors(service: ProfessorService = Depends(lambda: professor_service)):
    professors = await service.get_professors()

    formatted_professors = [
        {
            "id": str(professor["_id"]),  # Convertir ObjectId a string
            "correo": professor["correo"],
            "nombre": professor["nombre"],
            "apellidos": professor["apellidos"],
            "universidad": professor.get("universidad", "Cenfotec"),
            "fecha_creacion": professor.get("fecha_creacion", datetime.utcnow()),
            "materias": [
                {"id": str(materia["id"]), "nombre": materia["nombre"]}
                for materia in professor.get("materias", []) if isinstance(materia, dict)
            ]
        }
        for professor in professors
    ]

    return formatted_professors

#Update
@router.put("/put/{professor_id}", response_model=str)
async def update_professor(professor_id: str, professor: ProfessorCreateSchema,service: ProfessorService = Depends(lambda: professor_service)):
    professor_dict = professor.dict()

    if "materias" in professor_dict:
        professor_dict["materias"] = [
            {"id": str(materia["id"]), "nombre": materia["nombre"]}
            for materia in professor_dict["materias"]
            if isinstance(materia, dict) and "id" in materia and "nombre" in materia
        ]


    result = await service.update_professor(professor_id, professor_dict)

    return f"Profesor con ID {professor_id} actualizado correctamente. ID: {result}"

#Delete
@router.delete("/delete/{professor_id}", response_model=str)
async def delete_professor(professor_id: str, service: ProfessorService = Depends(lambda: professor_service)):
    return await service.delete_professor(professor_id)