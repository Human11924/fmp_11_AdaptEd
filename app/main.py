
from fastapi import FastAPI
from app.user.router import router as User_router
from app.quiz.routes import router as Quiz_router
from app.course.routes import router as Course_router
from app.task.route import router as Task_router
# from app.api.chat import router as chat_router

# Импортируем все модели для регистрации в SQLAlchemy
from app.course.model import Course
from app.quiz.model import Quiz
from app.task.model import Task
from app.user.model import User
# Добавьте сюда импорты других моделей по необходимости

app = FastAPI(
    title="Online Courses API",
    description="API AdaptEd",
    version="1.0.0"
)

app.include_router(User_router)
app.include_router(Quiz_router)
app.include_router(Course_router)
app.include_router(Task_router)
# app.include_router(chat_router)


@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": "Learning Management System API",
        "version": "1.0.0",
        "status": "running"
    }