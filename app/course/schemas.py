from pydantic import BaseModel
from typing import Optional


class CourseBase(BaseModel):
    """Базовые поля курса"""
    title: str


class CourseCreate(CourseBase):
    """Схема для создания курса"""
    pass


class CourseUpdate(BaseModel):
    """Схема для обновления курса"""
    title: Optional[str] = None


class CourseResponse(CourseBase):
    """Схема ответа курса"""
    id: int
    
    class Config:
        from_attributes = True