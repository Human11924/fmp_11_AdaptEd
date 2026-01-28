

from pydantic import BaseModel
from typing import Optional


class QuizBase(BaseModel):
    """Базовые поля квиза"""
    title: str
    description: Optional[str] = None
    course_id: int


class QuizCreate(QuizBase):
    """Схема для создания квиза"""
    pass


class QuizUpdate(BaseModel):
    """Схема для обновления квиза"""
    title: Optional[str] = None
    description: Optional[str] = None
    course_id: Optional[int] = None


class QuizzResponse(QuizBase):
    """Схема ответа квиза"""
    id: int
    
    class Config:
        from_attributes = True