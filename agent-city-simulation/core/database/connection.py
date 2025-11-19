"""Database connection management for Agent City"""

import os
import asyncpg
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Manages PostgreSQL database connections"""

    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

        # Get database config from environment
        self.host = os.getenv('POSTGRES_HOST', 'localhost')
        self.port = int(os.getenv('POSTGRES_PORT', 5432))
        self.user = os.getenv('POSTGRES_USER', 'agent_user')
        self.password = os.getenv('POSTGRES_PASSWORD', 'secure_password_change_this')
        self.database = os.getenv('POSTGRES_DB', 'agent_city')

    async def connect(self, pool_size: int = 10):
        """
        Create connection pool

        Args:
            pool_size: Number of connections in pool
        """
        try:
            logger.info(f"Connecting to database: {self.host}:{self.port}/{self.database}")

            self.pool = await asyncpg.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                min_size=2,
                max_size=pool_size
            )

            logger.info("Database connection pool created successfully")

        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    async def disconnect(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")

    async def execute(self, query: str, *args):
        """
        Execute a query that doesn't return data

        Args:
            query: SQL query
            *args: Query parameters

        Returns:
            Status message
        """
        if not self.pool:
            raise RuntimeError("Database not connected. Call connect() first.")

        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query: str, *args):
        """
        Execute a query and fetch all results

        Args:
            query: SQL query
            *args: Query parameters

        Returns:
            List of records
        """
        if not self.pool:
            raise RuntimeError("Database not connected. Call connect() first.")

        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args):
        """
        Execute a query and fetch one result

        Args:
            query: SQL query
            *args: Query parameters

        Returns:
            Single record or None
        """
        if not self.pool:
            raise RuntimeError("Database not connected. Call connect() first.")

        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query: str, *args):
        """
        Execute a query and fetch a single value

        Args:
            query: SQL query
            *args: Query parameters

        Returns:
            Single value or None
        """
        if not self.pool:
            raise RuntimeError("Database not connected. Call connect() first.")

        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)


# Global database instance
db = DatabaseConnection()
