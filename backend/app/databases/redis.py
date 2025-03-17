import asyncio

import redis.asyncio as aioredis

from app.core.config import config
from app.core.logger import logger


class RedisClient:
    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls):
        """ Singleton pattern to ensure a single Redis connection """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = None
        return cls._instance

    async def _create_client(self):
        """ Create a Redis client """
        async with self._lock:
            if self.client is None:
                try:
                    self.client = await aioredis.from_url(
                        config.REDIS_URL,
                        decode_responses=True
                    )
                    logger.info("Redis client created")
                except Exception as e:
                    logger.error(f"Error creating Redis client: {e}")
                    self.client = None

    async def connect(self):
        """ Initialize the Redis connection if not already connected or lost """
        if self.client is None:
            await self._create_client()
        else:
            try:
                await self.client.ping()
            except Exception as e:
                logger.error(f"Redis connection error: {e}. Reconnecting...")
                await self.close()
                await self._create_client()

    async def get_client(self) -> aioredis.Redis:
        await self.connect()
        if self.client is None:
            raise ConnectionError("Redis is not available!")
        return self.client

    async def close(self):
        """ Close the Redis connection """
        if self.client:
            try:
                await self.client.close()
                logger.info("Redis client closed")
            except Exception as e:
                logger.error(f"Error closing Redis client: {e}")
            finally:
                self.client = None

    async def is_connected(self) -> bool:
        """ Check if Redis is connected """
        if self.client:
            try:
                await self.client.ping()
                return True
            except Exception:
                return False
        return False


# Global Redis client instance
redis_client = RedisClient()
