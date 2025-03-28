from datetime import datetime

from pydantic import BaseModel

from shared_models.kafka.enums import ValidationStatus


class UrlValidationKafkaMessage(BaseModel):
    original_url: str
    short_code: str


class UrlValidationResult(BaseModel):
    short_code: str
    original_url: str
    validation_status: ValidationStatus
    checked_at: datetime
    threat_types: list[str] = []
    details: str | None = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
