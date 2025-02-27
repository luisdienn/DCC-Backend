from app.repositories.professor_repository import ProfessorRepository
from app.models.professor_model import ProfessorModel

class ProfessorService:
    def __init__(self, repository: ProfessorRepository):
        self.repository = repository  # Inyectamos el repositorio

    async def get_professors(self):
        return await self.repository.get_all_professors() 

    async def search_professors(self, name: str):
        return await self.repository.get_professors_by_name_or_lastname(name)
