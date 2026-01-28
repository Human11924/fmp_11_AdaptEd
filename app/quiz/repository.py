from abc import abstractmethod
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository_base import BaseRepository
from app.quiz.model import Quiz


class QuizRepositoryInterface(BaseRepository):
    """Интерфейс репозитория для Quiz"""
    
    @abstractmethod
    async def get_by_course_id(self, session: AsyncSession, course_id: int) -> List[Quiz]:
        """Получить все квизы курса"""
        pass


class QuizRepository(QuizRepositoryInterface):
    """Репозиторий для работы с квизами"""
    
    model = Quiz  # Просто указываем модель как атрибут класса
    
    async def get_by_course_id(self, session: AsyncSession, course_id: int) -> List[Quiz]:
        """Получить все квизы курса"""
        stmt = select(Quiz).where(Quiz.course_id == course_id)
        result = await session.execute(stmt)
        return result.scalars().all()