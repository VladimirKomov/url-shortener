from datetime import datetime

from sqlalchemy import func, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.databases.postgresql import Base
from shared_models.kafka.enums import ValidationStatus


class ShortenedURL(Base):
    __tablename__ = "shortened_urls"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    original_url: Mapped[str] = mapped_column(nullable=False)
    short_code: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    clicks: Mapped[int] = mapped_column(default=0)

    validation_status: Mapped[ValidationStatus] = mapped_column(
        Enum(ValidationStatus),
        default=ValidationStatus.PENDING,
        nullable=False
    )
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=func.now())
