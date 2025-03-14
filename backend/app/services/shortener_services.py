import random
import string


from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.shortener_ropository import ShortenerRepository


class ShortenerServices:
    def __init__(self, db: AsyncSession):
        self.repo = ShortenerRepository(db)

    def generate_short_code(self, length: int = 6) -> str:
        """Generate short code"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    async def create_short_url(self, original_url: str) -> dict[str, str]:
        """Create short url"""
        short_code = self.generate_short_code()
        short_url = await self.repo.save_short_url(short_code, original_url)
        return {short_code: short_url.original_url}

    async def get_original_url(self, short_code: str) -> str:
        """Get original url"""
        url = await self.repo.get_short_code(short_code)
        return url.original_url if url else ""

    async def increment_clicks(self, short_code: str) -> None:
        """Increment clicks"""
        url = await self.repo.get_short_code(short_code)
        if url:
            url.clicks += 1
            await self.repo.update_url(url)

