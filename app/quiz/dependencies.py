from app.quiz.service import QuizService
from app.quiz.repository import QuizRepository

def get_quiz_service() -> QuizService:
    """Dependency для получения QuizService"""
    quiz_repository = QuizRepository()
    return QuizService(quiz_repository)