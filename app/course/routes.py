from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.course.dependencies import get_course_service
from app.course.schemas import CourseResponse, CourseCreate, CourseUpdate
from app.course.service import CourseService

router = APIRouter(
    prefix="/courses",
    tags=["courses"],
)

course_service = get_course_service()

@router.post("/", response_model=CourseResponse)
async def create_course(
    course_data: CourseCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создать новый курс"""
    try:
        course = await course_service.create_course(session, course_data.title)
        return course
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/", response_model=List[CourseResponse])
async def get_all_courses(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session)
):
    """Получить все курсы с пагинацией"""
    try:
        courses = await course_service.get_all_courses(session, skip=skip, limit=limit)
        return courses
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int = Path(..., gt=0, description="ID курса"),
    session: AsyncSession = Depends(get_async_session)
):
    """Получить курс по ID"""
    try:
        course = await course_service.get_course_by_id(session, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Курс не найден")
        return course
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/{course_id}/with-quizzes")
async def get_course_with_quizzes(
    course_id: int = Path(..., gt=0, description="ID курса"),
    session: AsyncSession = Depends(get_async_session)
):
    """Получить курс вместе со всеми его квизами"""
    try:
        course = await course_service.get_course_with_quizzes(session, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Курс не найден")
        
        # Формируем ответ с квизами
        return {
            "id": course.id,
            "title": course.title,
            "quizzes": [
                {
                    "id": quiz.id,
                    "title": quiz.title,
                    "description": quiz.description,
                    "course_id": quiz.course_id
                } for quiz in course.quizzes
            ]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_data: CourseUpdate,
    course_id: int = Path(..., gt=0, description="ID курса"),
    session: AsyncSession = Depends(get_async_session)
):
    """Обновить курс"""
    try:
        if not course_data.title:
            raise HTTPException(status_code=400, detail="Название курса обязательно")
        
        course = await course_service.update_course(session, course_id, course_data.title)
        if not course:
            raise HTTPException(status_code=404, detail="Курс не найден")
        return course
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.delete("/{course_id}")
async def delete_course(
    course_id: int = Path(..., gt=0, description="ID курса"),
    session: AsyncSession = Depends(get_async_session)
):
    """Удалить курс вместе со всеми связанными квизами (cascade delete)"""
    try:
        deleted = await course_service.delete_course(session, course_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Курс не найден")
        return {"message": "Курс и все связанные квизы успешно удалены"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
