from abc import abstractmethod
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository_base import BaseRepository
from app.user.model import User
from app.user.auth import verify_password


class UserRepositoryInterface(BaseRepository):
    """Интерфейс репозитория для User"""
    
    @abstractmethod
    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        """Получить пользователя по email"""
        pass
    
    @abstractmethod
    async def get_by_credentials(self, session: AsyncSession, email: str, plain_password: str) -> Optional[User]:
        """Получить пользователя по email и паролю"""
        pass


class UserRepository(UserRepositoryInterface):
    """Репозиторий для работы с пользователями"""
    
    model = User
    
    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        """Получить пользователя по email"""
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_credentials(self, session: AsyncSession, email: str, plain_password: str) -> Optional[User]:
        """Получить пользователя по email и паролю"""
        # Сначала находим пользователя по email
        user = await self.get_by_email(session, email)
        
        # Если пользователь найден, проверяем пароль
        if user and verify_password(plain_password, user.hashed_password):
            return user
        
        return None