from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRegister(BaseModel):
    """Схема для регистрации пользователя"""
    first_name: str = Field(..., min_length=1, max_length=50, description="Имя пользователя")
    last_name: str = Field(..., min_length=1, max_length=50, description="Фамилия пользователя")
    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=6, max_length=100, description="Пароль пользователя")


class UserLogin(BaseModel):
    """Схема для авторизации пользователя"""
    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=1, description="Пароль пользователя")


class UserResponse(BaseModel):
    """Схема ответа с информацией о пользователе"""
    id: int
    first_name: str
    last_name: str
    email: str
    business_id: Optional[int] = None
    
    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Схема ответа при успешной авторизации"""
    access_token: str
    message: str = "Авторизация прошла успешно"


# Для совместимости с существующим кодом
SUser_register = UserRegister
SUser_login = UserLogin  
SUser_profile = UserResponse