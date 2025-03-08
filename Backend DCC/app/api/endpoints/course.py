from fastapi import APIRouter, Depends, HTTPException
from app.schemas.course_schema import CourseResponseSchema
from app.services.course_service import CourseService
from app.core.database import courses_collection
from app.repositories.course_repository import CourseRepository

router = APIRouter()

# Crear instancias de repositorio y servicio
course_repo = CourseRepository(courses_collection)
course_service = CourseService(course_repo)

#Create
@router.post("/create", response_model=str)
async def create_course(course: CourseResponseSchema, service: CourseService = Depends(lambda: course_service)):
    return await service.create_course(course)
              
#Read
@router.get("/", response_model=list[CourseResponseSchema])
async def get_all_courses(service: CourseService = Depends(lambda: course_service)):
    return await service.get_all_courses()

@router.get("/{course_id}", response_model=CourseResponseSchema)
async def get_course_by_id(course_id: str, service: CourseService = Depends(lambda: course_service)):
    return await service.get_course_by_id(course_id)

#Update
@router.put("/{course_id}", response_model=str)
async def update_course(course_id: str, course: CourseResponseSchema, service: CourseService = Depends(lambda: course_service)):
    return await service.update_course(course_id, course)

#Delete
@router.delete("/{course_id}", response_model=str)
async def delete_course(course_id: str, service: CourseService = Depends(lambda: course_service)):
    return await service.delete_course(course_id)