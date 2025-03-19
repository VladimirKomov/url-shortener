import redis.asyncio as aioredis

from app.core.config import config
from app.core.logger import logger
from app.databases.base_client import BaseAsyncClient


class RedisClient(BaseAsyncClient):
    """ Redis Client """

    async def _ping(self) -> bool:
        """ Check Redis connection """
        try:
            return await self.client.ping()
        except Exception:
            return False

    async def _create_client(self) -> None:
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

    async def _close_client(self) -> None:
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
