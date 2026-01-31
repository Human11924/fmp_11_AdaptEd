

from fastapi import APIRouter, Depends

from app.database import get_async_session
from app.task.dependencies import get_task_service


router = APIRouter(
    prefix = "/task",
    tags= ["task"]
)

task_service = get_task_service()

@router.get("/")
async def get_all_tasks(session = Depends(get_async_session)):
    tasks = await task_service.get_all_tasks(session)
    return tasks