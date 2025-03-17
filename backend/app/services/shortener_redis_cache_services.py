from aioredis import Redis
from typing_extensions import Optional

from app.databases.redis import redis_client


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
        return await client.get(key)

    async def set(self, key: str, value: str, ttl: int = 3600) -> bool:
        """Set value to redis"""
        client = await self._get_client()
        return await client.setex(key, ttl, value)

    async def delete(self, key: str) -> bool:
        """Delete value from redis"""
        client = await self._get_client()
        return await client.delete(key)
