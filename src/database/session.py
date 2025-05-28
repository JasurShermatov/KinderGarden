from contextlib import asynccontextmanager
from functools import cache
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)

# Updated import for the new structure
from src.config.settings import get_settings, Settings

# Get settings instance
settings: Settings = get_settings()


@cache
def get_async_engine() -> AsyncEngine:
    """Creates and returns a cached SQLAlchemy async engine instance."""
    return create_async_engine(
        "postgresql+asyncpg://"
        + settings.postgres_dsn,  # Use the DSN property from settings
        pool_size=10,  # Adjusted pool size, consider tuning based on load
        max_overflow=20,  # Adjusted max overflow
        future=True,
        echo=False,  # Set to True for debugging SQL queries
    )


@cache
def get_async_session_maker() -> async_sessionmaker[AsyncSession]:
    """Creates and returns a cached SQLAlchemy async session factory."""
    engine = get_async_engine()
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,  # Explicitly specify AsyncSession class
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,  # Recommended for async usage
    )


# Dependency for FastAPI routes
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that provides a database session per request."""
    session_maker = get_async_session_maker()
    async with session_maker() as session:
        try:
            yield session
            # Implicitly commits if no exceptions were raised and session was used
            # await session.commit() # Explicit commit if needed, but often handled by context manager
        except Exception:
            await session.rollback()  # Rollback on exceptions
            raise
        finally:
            await session.close()  # Ensure session is closed


# Context manager for use outside of FastAPI request cycle (e.g., background tasks)
@asynccontextmanager
async def get_standalone_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides a database session usable outside of FastAPI requests (e.g., Celery tasks)."""
    session_maker = get_async_session_maker()
    async with session_maker() as session:
        try:
            yield session
            await session.commit()  # Explicit commit is often needed in background tasks
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
