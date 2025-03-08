from app.repositories.course_repository import CourseRepository
from app.models.courses_model import CoursesModel

class CourseService:
    def __init__(self, repository: CourseRepository):
        self.repository = repository  # Inyectamos el repositorio


    #create
    async def create_course(self, course: CoursesModel):
        return await self.repository.create_course(course)

    #read
    async def get_course_by_id(self, id_course: int):
        return await self.repository.get_course_by_id(id_course)
    
    async def get_all_courses(self):
        return await self.repository.get_all_courses() 

    #update
    async def update_course(self, id_course: int, course: CoursesModel):
        return await self.repository.update_course(id_course, course)
    
    #delete
    async def delete_course(self, id_course: int):
        return await self.repository.delete_course(id_course)

