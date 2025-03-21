from datetime import datetime

from sqlalchemy import func, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.databases.postgresql import Base


class ShortenedURL(Base):
    __tablename__ = "shortened_urls"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    original_url: Mapped[str] = mapped_column(nullable=False)
    short_code: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    clicks: Mapped[int] = mapped_column(default=0)

    is_valid: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=func.now())
