"""
Database connection management with async support.

Provides connection pooling, retry logic, and health checks for PostgreSQL.
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from sqlalchemy import create_engine, event, pool, text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker

from core.shared.config import get_settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and sessions."""

    def __init__(self):
        """Initialize database manager."""
        self.settings = get_settings()
        self._async_engine: Optional[AsyncEngine] = None
        self._sync_engine: Optional[AsyncEngine] = None
        self._async_session_factory: Optional[async_sessionmaker] = None
        self._sync_session_factory: Optional[sessionmaker] = None

    async def initialize(self) -> None:
        """Initialize database connections and create session factories."""
        logger.info("Initializing database connections...")

        # Create async engine
        self._async_engine = create_async_engine(
            self.settings.database_url,
            poolclass=pool.AsyncAdaptedQueuePool,
            pool_size=self.settings.db_pool_size,
            max_overflow=self.settings.db_max_overflow,
            pool_pre_ping=True,  # Verify connections before using
            echo=self.settings.debug,
        )

        # Create sync engine (for migrations and admin tasks)
        self._sync_engine = create_engine(
            self.settings.database_url_sync,
            poolclass=pool.QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            echo=self.settings.debug,
        )

        # Create session factories
        self._async_session_factory = async_sessionmaker(
            self._async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        self._sync_session_factory = sessionmaker(
            self._sync_engine,
            class_=Session,
            expire_on_commit=False,
        )

        # Verify connection
        await self.health_check()
        logger.info("Database connections initialized successfully")

    async def close(self) -> None:
        """Close all database connections."""
        logger.info("Closing database connections...")

        if self._async_engine:
            await self._async_engine.dispose()

        if self._sync_engine:
            self._sync_engine.dispose()

        logger.info("Database connections closed")

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get an async database session.

        Yields:
            AsyncSession: Database session

        Example:
            async with db_manager.session() as session:
                result = await session.execute(query)
        """
        if not self._async_session_factory:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        session = self._async_session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    def sync_session(self) -> Session:
        """Get a synchronous database session.

        Returns:
            Session: Synchronous database session

        Example:
            with db_manager.sync_session() as session:
                result = session.execute(query)
        """
        if not self._sync_session_factory:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        return self._sync_session_factory()

    async def health_check(self) -> bool:
        """Check database connection health.

        Returns:
            bool: True if database is healthy, False otherwise
        """
        try:
            if not self._async_engine:
                return False

            async with self._async_engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                return True

        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

    async def retry_with_backoff(
        self,
        func,
        max_retries: int = 5,
        initial_delay: float = 1.0,
        backoff_factor: float = 2.0,
    ):
        """Retry a database operation with exponential backoff.

        Args:
            func: Async function to retry
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay in seconds
            backoff_factor: Multiplier for delay on each retry

        Returns:
            Result of the function

        Raises:
            Exception: If all retries fail
        """
        delay = initial_delay

        for attempt in range(max_retries):
            try:
                return await func()
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"All {max_retries} retry attempts failed")
                    raise

                logger.warning(
                    f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s..."
                )
                await asyncio.sleep(delay)
                delay *= backoff_factor

    @property
    def async_engine(self) -> AsyncEngine:
        """Get the async database engine."""
        if not self._async_engine:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._async_engine

    @property
    def sync_engine(self):
        """Get the sync database engine."""
        if not self._sync_engine:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._sync_engine


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


async def get_db() -> DatabaseManager:
    """Get the global database manager instance.

    Returns:
        DatabaseManager: Global database manager

    Example:
        db = await get_db()
        async with db.session() as session:
            ...
    """
    global _db_manager

    if _db_manager is None:
        _db_manager = DatabaseManager()
        await _db_manager.initialize()

    return _db_manager


async def close_db() -> None:
    """Close the global database manager."""
    global _db_manager

    if _db_manager:
        await _db_manager.close()
        _db_manager = None
