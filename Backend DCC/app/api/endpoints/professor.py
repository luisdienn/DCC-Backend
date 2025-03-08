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




#Create
@router.post("/create", response_model=str)
async def create_professor(professor: ProfessorResponseSchema, service: ProfessorService = Depends(lambda: professor_service)):
    return await service.create_professor(professor)
              
#Read
@router.get("/{professor_id}", response_model=ProfessorResponseSchema)
async def get_professor(professor_id: str, service: ProfessorService = Depends(lambda: professor_service)):
    return await service.get_professor_by_id(professor_id)

@router.get("/", response_model=list[ProfessorResponseSchema])
async def get_all_professors(service: ProfessorService = Depends(lambda: professor_service)):
    return await service.get_professors()

#Update
@router.put("/{professor_id}", response_model=str)
async def update_professor(professor_id: str, professor: ProfessorResponseSchema, service: ProfessorService = Depends(lambda: professor_service)):
    return await service.update_professor(professor_id, professor)

#Delete
@router.delete("/{professor_id}", response_model=str)
async def delete_professor(professor_id: str, service: ProfessorService = Depends(lambda: professor_service)):
    return await service.delete_professor(professor_id)