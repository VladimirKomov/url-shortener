from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.databases.db import Base


class ShortenedURL(Base):
    __tablename__ = "shortened_urls"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    original_url: Mapped[str] = mapped_column(nullable=False)
    short_code: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    clicks: Mapped[int] = mapped_column(default=0)

    created_at: Mapped[datetime] = mapped_column(default=func.now())
