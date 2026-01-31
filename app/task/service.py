

from app.task.repository import TaskRepository
from app.database import AsyncSession

class TaskService:
    def __init__(self ,task_repository:TaskRepository):
        self.task_repo = task_repository

    async def get_all_tasks(self, session:AsyncSession):
        tasks = await self.task_repo.get_all(session)
        return tasks