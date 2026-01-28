

from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.quiz.dependencies import get_quiz_service
from app.quiz.schemas import QuizzResponse, QuizCreate, QuizUpdate
from app.quiz.service import QuizService

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
)
quiz_service = get_quiz_service()

@router.get("/course/{course_id}/quizzes", response_model=List[QuizzResponse])
async def get_course_quizzes(
    course_id: int = Path(..., gt=0, description="ID курса"),
    session: AsyncSession = Depends(get_async_session)
):
    """Получить все квизы для курса"""
    try:
        quizzes = await quiz_service.get_quizzes_by_course(session, course_id)
        return quizzes
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.post("/", response_model=QuizzResponse)
async def create_quiz(
    quiz_data: QuizCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создать новый квиз"""
    try:
        quiz = await quiz_service.create_quiz(
            session, 
            quiz_data.title, 
            quiz_data.description,
            quiz_data.course_id
        )
        return quiz
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/{quiz_id}", response_model=QuizzResponse)
async def get_quiz(
    quiz_id: int = Path(..., gt=0, description="ID квиза"),
    session: AsyncSession = Depends(get_async_session)
):
    """Получить квиз по ID"""
    try:
        quiz = await quiz_service.get_quiz_by_id(session, quiz_id)
        if not quiz:
            raise HTTPException(status_code=404, detail="Квиз не найден")
        return quiz
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.put("/{quiz_id}", response_model=QuizzResponse)
async def update_quiz(
    quiz_data: QuizUpdate,
    quiz_id: int = Path(..., gt=0, description="ID квиза"),
    session: AsyncSession = Depends(get_async_session)
):
    """Обновить квиз"""
    try:
        update_dict = quiz_data.model_dump(exclude_unset=True)
        quiz = await quiz_service.update_quiz(session, quiz_id, **update_dict)
        if not quiz:
            raise HTTPException(status_code=404, detail="Квиз не найден")
        return quiz
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/{quiz_id}/with-course")
async def get_quiz_with_course(
    quiz_id: int = Path(..., gt=0, description="ID квиза"),
    session: AsyncSession = Depends(get_async_session)
):
    """Получить квиз вместе с информацией о курсе"""
    try:
        quiz = await quiz_service.get_quiz_with_course(session, quiz_id)
        if not quiz:
            raise HTTPException(status_code=404, detail="Квиз не найден")
        
        # Формируем ответ с курсом
        return {
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "course_id": quiz.course_id,
            "course": {
                "id": quiz.course.id,
                "title": quiz.course.title
            } if quiz.course else None
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.delete("/{quiz_id}")
async def delete_quiz(
    quiz_id: int = Path(..., gt=0, description="ID квиза"),
    session: AsyncSession = Depends(get_async_session)
):
    """Удалить квиз"""
    try:
        deleted = await quiz_service.delete_quiz(session, quiz_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Квиз не найден")
        return {"message": "Квиз успешно удален"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")  