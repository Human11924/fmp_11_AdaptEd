from app.course.service import CourseService
from app.course.repository import CourseRepository

def get_course_service() -> CourseService:
    """Dependency для получения CourseService"""
    course_repository = CourseRepository()
    return CourseService(course_repository)