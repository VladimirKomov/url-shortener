import random
import string

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import config
from app.core.exceptions import URLNotFoundException
from app.mappers.shortener_mapper import ShortenerMapper
from app.repositories.shortener_ropository import ShortenerRepository
from app.schemas.shortener_schemas import ShortenResponse, URLStatsResponse
from app.services.helpers.shortener_kafka_producer_services import ShortenerKafkaProducerService
from app.services.helpers.shortener_redis_cache_services import ShortenerRedisCacheServices
from app.interfaces.shortener_interfaces import AbstractShortenerService


class PostgresShortenerService(AbstractShortenerService):
    """Shortener services"""
    def __init__(self, db: AsyncSession):
        self.repo = ShortenerRepository(db)
        self.cache = ShortenerRedisCacheServices()
        self.kafka_producer = ShortenerKafkaProducerService()

    async def _generate_short_code(self, length: int = 6) -> str:
        """Generate short code"""
        while True:
            short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            existing_url = await self.repo.get_url_by_short_code(short_code)
            if not existing_url:
                return short_code

    async def _get_url_from_cache_or_db(self, short_code: str, background_tasks: BackgroundTasks) -> str:
        """Get url from cache or db"""
        cached_url = await self.cache.get(short_code)
        if cached_url:
            return cached_url

        url = await self.repo.get_url_by_short_code(short_code)
        if not url:
            raise URLNotFoundException()

        await self._save_to_cache(short_code, url.original_url)
        return url.original_url

    async def _save_to_cache(self, short_code: str, original_url: str) -> None:
        """Save to cache"""
        await self.cache.set(short_code, original_url)

    async def _update_clicks(self, short_code: str) -> None:
        """Update clicks"""
        url = await self.repo.get_url_by_short_code(short_code)
        if url:
            url.clicks += 1
            await self.repo.update_url(url)

    async def create_short_url(self, original_url: str, background_tasks: BackgroundTasks) -> ShortenResponse:
        """Create short url"""
        existing_url = await self.repo.get_url_by_long_url(original_url)
        if existing_url:
            return ShortenerMapper.to_short_response(existing_url, config.BASE_URL)

        short_code = await self._generate_short_code()
        # save to db
        short_url = await self.repo.save_url(short_code, original_url)
        # save to cache
        #await self._save_to_cache(short_code, original_url)
        # send to Kafka for validation (async validation)
        background_tasks.add_task(
            self.kafka_producer.send_url_validation, short_code, original_url
        )

        return ShortenerMapper.to_short_response(short_url, config.BASE_URL)

    async def get_original_url(self, short_code: str, background_tasks: BackgroundTasks) -> str:
        """Get original url"""
        original_url = await self._get_url_from_cache_or_db(
            short_code,
            background_tasks
        )
        background_tasks.add_task(self._update_clicks, short_code)
        return original_url

    async def get_stats(self, short_code: str) -> URLStatsResponse:
        """Get stats"""
        url = await self.repo.get_url_by_short_code(short_code)
        if not url:
            raise URLNotFoundException()
        return ShortenerMapper.to_url_stats_response(url)

    async def delete_short_url(self, short_code: str) -> bool:
        """Delete short url"""
        await self.cache.delete(short_code)
        success = await self.repo.delete_url(short_code)
        if not success:
            raise URLNotFoundException()
        return success
