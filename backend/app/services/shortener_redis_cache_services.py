from typing_extensions import Optional

from app.databases.redis import redis_client


class ShortenerRedisCacheServices:

    def __init__(self):
        self.client  = None

    async def _get_client(self):
        if self.client is None:
            self.client = await redis_client.get_client()
        return self.client

    async def get(self, key: str) -> Optional[str]:
        """Get value from redis"""
        client = await self._get_client()
        return await client.get(key)

    async def set(self, key: str, value: str, ttl: int = 3600) -> None:
        """Set value to redis"""
        client = await self._get_client()
        await client.setex(key, ttl, value)

    async def delete(self, key: str) -> None:
        """Delete value from redis"""
        client = await self._get_client()
        await client.delete(key)
