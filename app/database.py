from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker , DeclarativeBase
from app.config import db_url

DATABASE_URL = db_url
engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine , class_= AsyncSession, expire_on_commit = False )


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncSession:
    """Dependency для получения async сессии"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()