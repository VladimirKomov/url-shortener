from redis.asyncio import Redis
from typing_extensions import Optional

from app.databases.redis import redis_client
from app.core.logger import logger


class ShortenerRedisCacheServices:

    def __init__(self):
        self.client = None

    async def _get_client(self) -> Redis:
        if self.client is None:
            self.client = await redis_client.get_client()
        return self.client

    async def get(self, key: str) -> Optional[str]:
        """Get value from redis"""
        client = await self._get_client()
        url =  await client.get(key)
        if not url:
            logger.info(f"{key} not found in redis")
        logger.info(f"Getting {key} from redis")
        return url

    async def set(self, key: str, value: str, ttl: int = 3600) -> bool:
        """Set value to redis"""
        client = await self._get_client()
        success = await client.setex(key, ttl, value)
        if success is None or success is False:
            logger.error(f"Error setting {key} to redis")
            return False
        logger.info(f"Setting {key} to redis")
        return True

    async def delete(self, key: str) -> bool:
        """Delete value from redis"""
        client = await self._get_client()
        success = await client.delete(key)
        if not success:
            logger.warning(f"Error deleting {key} from redis")
        logger.info(f"Deleting {key} from redis")
        return success
