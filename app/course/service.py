from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.course.model import Course
from app.course.repository import CourseRepositoryInterface
from app.quiz.model import Quiz


class CourseService:
    """Сервис для бизнес-логики курсов"""
    
    def __init__(self, course_repository: CourseRepositoryInterface):
        self.course_repository = course_repository
    
    async def create_course(self, session: AsyncSession, title: str) -> Course:
        """Создать новый курс"""
        if not title or len(title.strip()) < 3:
            raise ValueError("Название курса должно содержать минимум 3 символа")
        
        # Проверяем, что курс с таким названием не существует
        existing_course = await self.course_repository.get_by_title(session, title.strip())
        if existing_course:
            raise ValueError("Курс с таким названием уже существует")
        
        return await self.course_repository.create(session, title=title.strip())
    
    async def get_course_by_id(self, session: AsyncSession, course_id: int) -> Optional[Course]:
        """Получить курс по ID"""
        if course_id <= 0:
            raise ValueError("Course ID должен быть положительным числом")
        
        return await self.course_repository.get_by_id(session, course_id)
    
    async def get_course_with_quizzes(self, session: AsyncSession, course_id: int) -> Optional[Course]:
        """Получить курс вместе со всеми его квизами"""
        if course_id <= 0:
            raise ValueError("Course ID должен быть положительным числом")
        
        from sqlalchemy.orm import selectinload
        stmt = select(Course).options(selectinload(Course.quizzes)).where(Course.id == course_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all_courses(self, session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Course]:
        """Получить все курсы с пагинацией"""
        if skip < 0:
            raise ValueError("Skip должен быть неотрицательным")
        if limit <= 0 or limit > 1000:
            raise ValueError("Limit должен быть от 1 до 1000")
        
        return await self.course_repository.get_all(session, skip=skip, limit=limit)
    
    async def update_course(self, session: AsyncSession, course_id: int, title: str) -> Optional[Course]:
        """Обновить курс"""
        if course_id <= 0:
            raise ValueError("Course ID должен быть положительным числом")
        if not title or len(title.strip()) < 3:
            raise ValueError("Название курса должно содержать минимум 3 символа")
        
        return await self.course_repository.update(session, course_id, title=title.strip())
    
    async def delete_course(self, session: AsyncSession, course_id: int) -> bool:
        """Удалить курс вместе со всеми квизами (ручное удаление связанных записей)"""
        if course_id <= 0:
            raise ValueError("Course ID должен быть положительным числом")
        
        # Проверяем существование курса
        course = await self.course_repository.get_by_id(session, course_id)
        if not course:
            return False
        
        # Сначала удаляем все квизы этого курса
        from sqlalchemy import delete
        from app.quiz.model import Quiz
        
        delete_quizzes_stmt = delete(Quiz).where(Quiz.course_id == course_id)
        await session.execute(delete_quizzes_stmt)
        
        # Теперь удаляем сам курс
        return await self.course_repository.delete(session, course_id)