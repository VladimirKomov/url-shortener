import random
import string

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.config import config
from app.mappers.shortener_mapper import ShortenerMapper
from app.repositories.shortener_ropository import ShortenerRepository
from app.schemas.shortener_schemas import ShortenResponse


class ShortenerServices:
    def __init__(self, db: AsyncSession):
        self.repo = ShortenerRepository(db)

    async def _generate_short_code(self, length: int = 6) -> str:
        """Generate short code"""
        while True:
            short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            existing_url = await self.repo.get_url_by_short_code(short_code)
            if not existing_url:
                return short_code

    async def _increment_clicks(self, short_code: str) -> None:
        """Increment clicks"""
        url = await self.repo.get_url_by_short_code(short_code)
        if url:
            url.clicks += 1
            await self.repo.update_url(url)

    async def create_short_url(self, original_url: str) -> ShortenResponse:
        """Create short url"""
        existing_url = await self.repo.get_url_by_long_url(original_url)
        if existing_url:
            return ShortenerMapper.to_short_response(existing_url, config.BASE_URL)

        short_code = await self._generate_short_code()
        short_url = await self.repo.save_url(short_code, original_url)
        return ShortenerMapper.to_short_response(short_url, config.BASE_URL)

    async def get_original_url(self, short_code: str) -> str:
        """Get original url"""
        url = await self.repo.get_url_by_short_code(short_code)

        if not url:
            raise HTTPException(status_code=404, detail="URL not found")
        else:
            await self._increment_clicks(short_code)

        return url.original_url

    async def get_stats(self, short_code: str) -> int:
        """Get stats"""
        url = await self.repo.get_url_by_short_code(short_code)
        return url.clicks if url else 0

    async def delete_short_url(self, short_code: str) -> bool:
        """Delete short url"""
        return await self.repo.delete_url(short_code)
