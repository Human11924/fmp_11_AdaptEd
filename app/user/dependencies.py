from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import Settings
from app.database import get_async_session
from app.user.service import UserService
from app.user.repository import UserRepository
  
settings = Settings()

def get_user_service() -> UserService:
    """Dependency для получения UserService"""
    user_repository = UserRepository()
    return UserService(user_repository)

def get_access_token(request: Request):
    token = request.cookies.get("user_access_token")
    if token:
        return token
    raise HTTPException(status_code=401, detail="Токен доступа не найден")

async def get_current_user(
    token: str = Depends(get_access_token),
    session: AsyncSession = Depends(get_async_session),
    user_service: UserService = Depends(get_user_service)
):
    """Получить текущего пользователя из JWT токена"""
    try:
        access = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        user_id: str = access.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Неверный токен")
            
        user = await user_service.get_user_by_id(session, int(user_id))

        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")
            
        return user
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Неверный токен")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при получении пользователя")
