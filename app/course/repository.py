from abc import abstractmethod
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository_base import BaseRepository
from app.course.model import Course


class CourseRepositoryInterface(BaseRepository):
    """Интерфейс репозитория для Course"""
    
    @abstractmethod
    async def get_by_title(self, session: AsyncSession, title: str) -> Optional[Course]:
        """Получить курс по названию"""
        pass


class CourseRepository(CourseRepositoryInterface):
    """Репозиторий для работы с курсами"""
    
    model = Course  # Просто указываем модель как атрибут класса
    
    async def get_by_title(self, session: AsyncSession, title: str) -> Optional[Course]:
        """Получить курс по названию"""
        stmt = select(Course).where(Course.title == title)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()