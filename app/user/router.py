
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session

from app.user.dependencies import get_current_user, get_user_service
from app.user.schema import UserRegister, UserLogin, UserResponse, LoginResponse
from app.user.service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/register",response_model = UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister,
    session: AsyncSession = Depends(get_async_session),
    user_service: UserService = Depends(get_user_service)
):
    """Регистрация нового пользователя"""
    try:
        user = await user_service.register_user(
            session,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password=user_data.password  # Теперь пароль будет захеширован в сервисе
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500,detail = str(e))


@router.post("/login", response_model=LoginResponse)
async def login_user(
    response: Response,
    user_data: UserLogin,
    session: AsyncSession = Depends(get_async_session),
    user_service: UserService = Depends(get_user_service)
):
    """Авторизация пользователя"""
    try:
        access_token = await user_service.login_user(
            session,
            email=user_data.email,
            password=user_data.password  # Теперь пароль будет захеширован в сервисе
        )
        
        # Устанавливаем cookie с токеном
        response.set_cookie(
            "user_access_token", 
            access_token, 
            httponly=True,
            secure=True,  # В продакшене должно быть True
            samesite="lax"
        )
        
        return LoginResponse(access_token=access_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user = Depends(get_current_user)):
    """Получение профиля текущего пользователя"""
    return current_user


@router.post("/logout")
async def logout_user(response: Response):
    """Выход пользователя из системы"""
    response.delete_cookie("user_access_token")
    return {"message": "Успешный выход из системы"}