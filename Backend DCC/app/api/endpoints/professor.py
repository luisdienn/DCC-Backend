from fastapi import APIRouter, Depends, HTTPException
from app.schemas.professor_schema import ProfessorResponseSchema
from app.services.professor_service import ProfessorService
from app.core.database import professors_collection
from app.repositories.professor_repository import ProfessorRepository

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

@router.get("/", response_model=list[ProfessorResponseSchema])
async def get_all_professors(service: ProfessorService = Depends(lambda: professor_service)):
    return await service.get_professors()
