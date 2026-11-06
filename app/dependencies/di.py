from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.connection import get_session


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that yields an async database session per request."""
    async for session in get_session():
        yield session
