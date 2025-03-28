from datetime import datetime
from typing import Optional

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import ShortenedURL
from shared_models.kafka.enums import ValidationStatus


class ShortenerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_url_by_long_url(self, original_url: str) -> Optional[ShortenedURL]:
        """GET URL by original url"""
        result = await self.db.execute(
            select(ShortenedURL).where(
                ShortenedURL.original_url == original_url
            )
        )
        return result.scalars().first()

    async def get_url_by_short_code(self, short_code: str) -> Optional[ShortenedURL]:
        """GET URL by short code"""
        result = await self.db.execute(
            select(ShortenedURL).where(
                ShortenedURL.short_code == short_code
            )
        )
        return result.scalars().first()

    async def save_url(
            self,
            short_code: str,
            original_url: str,
            validation_status: ValidationStatus
    ) -> ShortenedURL:
        """Save short code"""
        new_url = ShortenedURL(
            short_code=short_code,
            original_url=original_url,
            validation_status=validation_status
        )
        self.db.add(new_url)
        await self.db.commit()
        await self.db.refresh(new_url)
        return new_url

    async def update_url(self, url: ShortenedURL) -> None:
        """Update url"""
        self.db.add(url)
        await self.db.commit()
        await self.db.refresh(url)

    async def increment_clicks(self, short_code: str) -> None:
        """Increment clicks"""
        await self.db.execute(
            update(ShortenedURL)
            .where(ShortenedURL.short_code == short_code)
            .values(clicks=ShortenedURL.clicks + 1)
        )
        await self.db.commit()

    async def set_url_valid_status(
            self,
            short_code: str,
            validation_status: ValidationStatus,
            checked_at: datetime
    ) -> None:
        """Set url valid status"""
        await self.db.execute(
            update(ShortenedURL)
            .where(ShortenedURL.short_code == short_code)
            .values(
                validation_status=validation_status,
                validated_at=checked_at
            )
        )
        await self.db.commit()

    async def delete_url(self, short_code: str) -> bool:
        """Delete short code"""
        result = await self.db.execute(
            delete(ShortenedURL).where(
                ShortenedURL.short_code == short_code
            )
        )
        await self.db.commit()
        return result.rowcount() > 0
