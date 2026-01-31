from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.user.model import User
from app.user.repository import UserRepositoryInterface
from app.user.auth import create_access_token, hash_password


class UserService:
    """Сервис для бизнес-логики пользователей"""
    
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository
    
    async def register_user(
        self, 
        session: AsyncSession, 
        first_name: str,
        last_name: str,
        email: str,
        password: str
    ) -> User:
        """Регистрация нового пользователя"""
        # Валидация данных
        if not email or not email.strip():
            raise ValueError("Электронный адрес обязателен")
        if not first_name or not first_name.strip():
            raise ValueError("Имя обязательно")
        if not last_name or not last_name.strip():
            raise ValueError("Фамилия обязательна")
        if not password or len(password.strip()) < 6:
            raise ValueError("Пароль должен быть не менее 6 символов")
        
        # Проверяем, что пользователь с таким email не существует
        existing_user = await self.user_repository.get_by_email(session, email.strip())
        if existing_user:
            raise ValueError("Пользователь с таким адресом электронной почты уже зарегистрирован")
        
        # Хешируем пароль
        hashed_password = hash_password(password.strip())
        
        return await self.user_repository.create(
            session,
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            email=email.strip(),
            hashed_password=hashed_password
        )
    
    async def login_user(
        self,
        session: AsyncSession,
        email: str,
        password: str
    ) -> str:
        """Авторизация пользователя"""
        if not email or not email.strip():
            raise ValueError("Email обязателен")
        if not password:
            raise ValueError("Пароль обязателен")
        
        user = await self.user_repository.get_by_credentials(
            session, 
            email.strip(), 
            password
        )
        
        if not user:
            raise ValueError("Неверный email или пароль")
        
        access_token = create_access_token({"sub": str(user.id)})
        return access_token
    
    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> Optional[User]:
        """Получить пользователя по ID"""
        if user_id <= 0:
            raise ValueError("User ID должен быть положительным числом")
        
        return await self.user_repository.get_by_id(session, user_id)
    
    async def get_user_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        """Получить пользователя по email"""
        if not email or not email.strip():
            raise ValueError("Email обязателен")
        
        return await self.user_repository.get_by_email(session, email.strip())