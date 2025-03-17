from app.repositories.professor_repository import ProfessorRepository
from app.models.professor_model import ProfessorModel

class ProfessorService:
    def __init__(self, repository: ProfessorRepository):
        self.repository = repository  # Inyectamos el repositorio


    async def search_professors(self, name: str):
        return await self.repository.get_professors_by_name_or_lastname(name)
    
    #create
    async def create_professor(self, professor_data: dict):
        professor_obj = ProfessorModel(**professor_data)  
        return await self.repository.create_professor(professor_obj)
    
    #read
    async def get_professor_by_id(self, professor_id: str):
        return await self.repository.get_professor_by_id(professor_id)
    
    async def get_professors(self):
        return await self.repository.get_all_professors()
    
    #update
    async def update_professor(self, professor_id: str, professor: ProfessorModel):
        return await self.repository.update_professor(professor_id, professor)
    
    #delete
    async def delete_professor(self, professor_id: str):
        return await self.repository.delete_professor(professor_id)
    
