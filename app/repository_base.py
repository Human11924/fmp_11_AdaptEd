from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')

class BaseRepository(ABC):
    """Базовый абстрактный репозиторий"""
    
    # Дочерние классы должны определить model
    model = None
    
    async def get_by_id(self, session: AsyncSession, id: int) -> Optional[T]:
        """Получить запись по ID"""
        stmt = select(self.model).where(self.model.id == id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(self, session: AsyncSession, skip: int = 0, limit: int = 100) -> List[T]:
        """Получить все записи с пагинацией"""
        stmt = select(self.model).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()
    
    async def create(self, session: AsyncSession, **data) -> T:
        """Создать новую запись"""
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar_one()
    
    async def update(self, session: AsyncSession, id: int, **data) -> Optional[T]:
        """Обновить запись"""
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .returning(self.model)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar_one_or_none()
    
    async def delete(self, session: AsyncSession, id: int) -> bool:
        """Удалить запись"""
        stmt = delete(self.model).where(self.model.id == id)
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0
    
    async def find_by_filter(self, session: AsyncSession, **filters) -> List[T]:
        """Найти записи по фильтру"""
        stmt = select(self.model).filter_by(**filters)
        result = await session.execute(stmt)
        return result.scalars().all()