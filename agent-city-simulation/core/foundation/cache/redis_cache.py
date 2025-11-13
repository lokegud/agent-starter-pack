"""
Redis cache management.

Provides caching functionality with TTL, serialization, and health checks.
"""

import json
import logging
from typing import Any, Optional

import redis.asyncio as aioredis
from redis.asyncio import Redis

from core.shared.config import get_settings

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages Redis cache connections and operations."""

    def __init__(self):
        """Initialize cache manager."""
        self.settings = get_settings()
        self._redis: Optional[Redis] = None

    async def initialize(self) -> None:
        """Initialize Redis connection."""
        logger.info("Initializing Redis cache connection...")

        self._redis = await aioredis.from_url(
            self.settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=50,
        )

        # Verify connection
        await self.health_check()
        logger.info("Redis cache initialized successfully")

    async def close(self) -> None:
        """Close Redis connection."""
        if self._redis:
            logger.info("Closing Redis cache connection...")
            await self._redis.close()
            logger.info("Redis cache closed")

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        if not self._redis:
            raise RuntimeError("Cache not initialized. Call initialize() first.")

        try:
            value = await self._redis.get(key)
            if value:
                # Try to deserialize JSON
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return None

        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> bool:
        """Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (None = default TTL)

        Returns:
            True if successful, False otherwise
        """
        if not self._redis:
            raise RuntimeError("Cache not initialized. Call initialize() first.")

        try:
            # Serialize value to JSON if it's not a string
            if not isinstance(value, str):
                value = json.dumps(value)

            # Use default TTL if not provided
            if ttl is None:
                ttl = self.settings.cache_ttl

            await self._redis.setex(key, ttl, value)
            return True

        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete value from cache.

        Args:
            key: Cache key

        Returns:
            True if deleted, False otherwise
        """
        if not self._redis:
            raise RuntimeError("Cache not initialized. Call initialize() first.")

        try:
            result = await self._redis.delete(key)
            return result > 0

        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache.

        Args:
            key: Cache key

        Returns:
            True if key exists, False otherwise
        """
        if not self._redis:
            raise RuntimeError("Cache not initialized. Call initialize() first.")

        try:
            result = await self._redis.exists(key)
            return result > 0

        except Exception as e:
            logger.error(f"Cache exists error for key {key}: {e}")
            return False

    async def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment a counter in cache.

        Args:
            key: Cache key
            amount: Amount to increment by

        Returns:
            New value after increment
        """
        if not self._redis:
            raise RuntimeError("Cache not initialized. Call initialize() first.")

        try:
            return await self._redis.incrby(key, amount)

        except Exception as e:
            logger.error(f"Cache increment error for key {key}: {e}")
            return None

    async def set_hash(self, key: str, mapping: dict) -> bool:
        """Set multiple fields in a hash.

        Args:
            key: Hash key
            mapping: Dictionary of field:value pairs

        Returns:
            True if successful, False otherwise
        """
        if not self._redis:
            raise RuntimeError("Cache not initialized. Call initialize() first.")

        try:
            # Serialize complex values
            serialized_mapping = {}
            for field, value in mapping.items():
                if isinstance(value, (dict, list)):
                    serialized_mapping[field] = json.dumps(value)
                else:
                    serialized_mapping[field] = str(value)

            await self._redis.hset(key, mapping=serialized_mapping)
            return True

        except Exception as e:
            logger.error(f"Cache set_hash error for key {key}: {e}")
            return False

    async def get_hash(self, key: str, field: str) -> Optional[Any]:
        """Get a field from a hash.

        Args:
            key: Hash key
            field: Field name

        Returns:
            Field value or None if not found
        """
        if not self._redis:
            raise RuntimeError("Cache not initialized. Call initialize() first.")

        try:
            value = await self._redis.hget(key, field)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return None

        except Exception as e:
            logger.error(f"Cache get_hash error for key {key}, field {field}: {e}")
            return None

    async def get_all_hash(self, key: str) -> Optional[dict]:
        """Get all fields from a hash.

        Args:
            key: Hash key

        Returns:
            Dictionary of field:value pairs
        """
        if not self._redis:
            raise RuntimeError("Cache not initialized. Call initialize() first.")

        try:
            data = await self._redis.hgetall(key)
            if not data:
                return None

            # Deserialize values
            result = {}
            for field, value in data.items():
                try:
                    result[field] = json.loads(value)
                except json.JSONDecodeError:
                    result[field] = value

            return result

        except Exception as e:
            logger.error(f"Cache get_all_hash error for key {key}: {e}")
            return None

    async def push_to_list(self, key: str, *values: Any) -> bool:
        """Push values to the end of a list.

        Args:
            key: List key
            *values: Values to push

        Returns:
            True if successful, False otherwise
        """
        if not self._redis:
            raise RuntimeError("Cache not initialized. Call initialize() first.")

        try:
            # Serialize values
            serialized_values = []
            for value in values:
                if isinstance(value, (dict, list)):
                    serialized_values.append(json.dumps(value))
                else:
                    serialized_values.append(str(value))

            await self._redis.rpush(key, *serialized_values)
            return True

        except Exception as e:
            logger.error(f"Cache push_to_list error for key {key}: {e}")
            return False

    async def get_list_range(
        self,
        key: str,
        start: int = 0,
        end: int = -1,
    ) -> Optional[list]:
        """Get a range of values from a list.

        Args:
            key: List key
            start: Start index
            end: End index (-1 = end of list)

        Returns:
            List of values
        """
        if not self._redis:
            raise RuntimeError("Cache not initialized. Call initialize() first.")

        try:
            values = await self._redis.lrange(key, start, end)
            if not values:
                return None

            # Deserialize values
            result = []
            for value in values:
                try:
                    result.append(json.loads(value))
                except json.JSONDecodeError:
                    result.append(value)

            return result

        except Exception as e:
            logger.error(f"Cache get_list_range error for key {key}: {e}")
            return None

    async def health_check(self) -> bool:
        """Check Redis connection health.

        Returns:
            True if Redis is healthy, False otherwise
        """
        try:
            if not self._redis:
                return False

            await self._redis.ping()
            return True

        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return False

    @property
    def redis(self) -> Redis:
        """Get the Redis client."""
        if not self._redis:
            raise RuntimeError("Cache not initialized. Call initialize() first.")
        return self._redis


# Global cache manager instance
_cache_manager: Optional[CacheManager] = None


async def get_cache() -> CacheManager:
    """Get the global cache manager instance.

    Returns:
        CacheManager: Global cache manager

    Example:
        cache = await get_cache()
        await cache.set("key", "value", ttl=300)
    """
    global _cache_manager

    if _cache_manager is None:
        _cache_manager = CacheManager()
        await _cache_manager.initialize()

    return _cache_manager


async def close_cache() -> None:
    """Close the global cache manager."""
    global _cache_manager

    if _cache_manager:
        await _cache_manager.close()
        _cache_manager = None
