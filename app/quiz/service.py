
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.quiz.model import Quiz
from app.quiz.repository import QuizRepositoryInterface


class QuizService:
    """Сервис для бизнес-логики квизов"""
    
    def __init__(self, quiz_repository: QuizRepositoryInterface):
        self.quiz_repository = quiz_repository
        
    async def get_quizzes_by_course(self, session: AsyncSession, course_id: int) -> List[Quiz]:
        """Получить все квизы для курса с бизнес-логикой"""
        if course_id <= 0:
            raise ValueError("Course ID должен быть положительным числом")
        
        quizzes = await self.quiz_repository.get_by_course_id(session, course_id)
        
        # Здесь может быть дополнительная бизнес-логика:
        # - фильтрация по правам доступа
        # - сортировка
        # - кэширование и т.д.
        
        return quizzes
    
    async def get_quiz_by_id(self, session: AsyncSession, quiz_id: int) -> Optional[Quiz]:
        """Получить квиз по ID"""
        if quiz_id <= 0:
            raise ValueError("Quiz ID должен быть положительным числом")
        
        return await self.quiz_repository.get_by_id(session, quiz_id)
    
    async def get_quiz_with_course(self, session: AsyncSession, quiz_id: int) -> Optional[Quiz]:
        """Получить квиз вместе с информацией о курсе через relationship"""
        if quiz_id <= 0:
            raise ValueError("Quiz ID должен быть положительным числом")
        
        # Используем selectinload для загрузки связанного курса
        from sqlalchemy.orm import selectinload
        from sqlalchemy import select
        
        stmt = select(Quiz).options(selectinload(Quiz.course)).where(Quiz.id == quiz_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create_quiz(self, session: AsyncSession, title: str, description: str, course_id: int) -> Quiz:
        """Создать новый квиз"""
        if not title or len(title.strip()) < 3:
            raise ValueError("Название квиза должно содержать минимум 3 символа")
        if course_id <= 0:
            raise ValueError("Course ID должен быть положительным числом")
        
        return await self.quiz_repository.create(
            session, 
            title=title.strip(), 
            description=description,
            course_id=course_id
        )
    
    async def update_quiz(self, session: AsyncSession, quiz_id: int, **data) -> Optional[Quiz]:
        """Обновить квиз"""
        if quiz_id <= 0:
            raise ValueError("Quiz ID должен быть положительным числом")
        
        return await self.quiz_repository.update(session, quiz_id, **data)
    
    async def delete_quiz(self, session: AsyncSession, quiz_id: int) -> bool:
        """Удалить квиз"""
        if quiz_id <= 0:
            raise ValueError("Quiz ID должен быть положительным числом")
        
        return await self.quiz_repository.delete(session, quiz_id)
        
        raise ValueError("Quiz ID должен быть положительным числом")
        
        return await self.quiz_repository.get_by_id(session, quiz_id)