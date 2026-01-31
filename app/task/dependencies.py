

from app.task.repository import TaskRepository
from app.task.service import TaskService


def get_task_service():
    task_repository = TaskRepository()
    return TaskService(task_repository)