from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import ShortenedURL


class ShortenerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_short_code(self, short_code: str) -> Optional[ShortenedURL]:
        """GET URL by short code"""
        result = await self.db.execute(
            select(ShortenedURL).where(
                ShortenedURL.short_code == short_code
            )
        )
        return result.scalars().first()

    async def save_short_url(self, short_code: str, original_url: str) -> ShortenedURL:
        """Save short code"""
        new_url = ShortenedURL(short_code=short_code, original_url=original_url)
        self.db.add(new_url)
        await self.db.commit()
        await self.db.refresh(new_url)
        return new_url

    async def update_url(self, url: ShortenedURL) -> None:
        """Update url"""
        self.db.add(url)
        await self.db.commit()
        await self.db.refresh(url)

    async def delete_short_url(self, short_code: str) -> bool:
        """Delete short code"""
        result = await self.db.execute(
            delete(ShortenedURL).where(
                ShortenedURL.short_code == short_code
            )
        )
        await self.db.commit()
        return result.rowcount() > 0
