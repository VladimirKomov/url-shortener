from datetime import datetime

from pydantic import BaseModel, HttpUrl


class UrlValidationKafkaMessage(BaseModel):
    original_url: HttpUrl
    short_code: str


class UrlValidationResult(BaseModel):
    short_code: str
    original_url: str
    is_safe: bool | None
    checked_at: datetime
    threat_types: list[str] = []
    details: str | None = None
