

from sqlalchemy import select
from app.repository_base import BaseRepository
from app.task.model import Task
from sqlalchemy.ext.asyncio import AsyncSession

class TaskRepository(BaseRepository):
    model = Task

    async def get_all(self, session: AsyncSession):
        query = select(Task)
        result = await session.execute(query)
        return result.scalars().all()