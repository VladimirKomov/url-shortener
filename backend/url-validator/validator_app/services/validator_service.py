from datetime import datetime
from shared_models.kafka.url_validation import UrlValidationKafkaMessage
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

from validator_app.services.helpers.google_service import GoogleUrlChecker


class UrlValidationResult(BaseModel):
    short_code: str
    original_url: str
    is_safe: bool
    checked_at: datetime
    inserted_at: datetime
    threat_types: list[str] = []
    details: str | None = None


class ValidatorService:
    def __init__(self, mongo_client: AsyncIOMotorClient, google_service: GoogleUrlChecker):
        self.mongo = mongo_client
        self.google_service = google_service

    async def handle_message(self, payload: UrlValidationKafkaMessage):
        result = await self.validate(payload)

        if result is not None:
            await self.mongo.url_validator.url_validations.insert_one(result.model_dump())
        else:
            # Optionally, log or store unvalidated payloads
            pass

    async def validate(self, payload: UrlValidationKafkaMessage) -> UrlValidationResult | None:
        # Use the updated method that returns (bool | None, list)
        is_safe, threats = await self.google_service.is_url_safe(str(payload.original_url))

        # If validation failed, skip storing result (or handle separately)
        if is_safe is None:
            return None

        return UrlValidationResult(
            short_code=payload.short_code,
            original_url=str(payload.original_url),
            is_safe=is_safe,
            checked_at=datetime.utcnow(),
            inserted_at=datetime.utcnow(),
            threat_types=[m["threatType"] for m in threats],
            details="Checked via Google Safe Browsing"
        )
