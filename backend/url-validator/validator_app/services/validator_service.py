from datetime import datetime
from shared_models.kafka.url_validation import UrlValidationKafkaMessage
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

from validator_app.repositories.url_validation_repository import UrlValidationRepository
from validator_app.services.helpers.validation_google_service import GoogleUrlChecker
from validator_app.services.helpers.validation_kafka_producer_services import ValidationResultProducerService


class UrlValidationResult(BaseModel):
    short_code: str
    original_url: str
    is_safe: bool | None
    checked_at: datetime
    threat_types: list[str] = []
    details: str | None = None


class ValidatorService:
    def __init__(
            self,
            mongo_repository: UrlValidationRepository,
            google_service: GoogleUrlChecker,
            kafka_producer_service: ValidationResultProducerService
    ):
        self.mongo = mongo_repository
        self.google_service = google_service
        self.kafka_producer_service = kafka_producer_service

    async def handle_message(self, payload: UrlValidationKafkaMessage):
        result: UrlValidationResult | None = await self.validate(payload)

        await self.mongo.save(result)
        await self.kafka_producer_service.send_url_validation_result(result)

    async def validate(self, payload: UrlValidationKafkaMessage) -> UrlValidationResult:
        # Use the updated method that returns (bool | None, list)
        # None - the check was not performed
        is_safe, threats = await self.google_service.is_url_safe(str(payload.original_url))

        details = (
            "Validation failed: Google Safe Browsing unavailable"
            if is_safe is None
            else "Checked via Google Safe Browsing"
        )

        # If validation failed, skip storing result (or handle separately)
        return UrlValidationResult(
            short_code=payload.short_code,
            original_url=str(payload.original_url),
            # None - the check was not performed
            is_safe=is_safe,
            checked_at=datetime.now(),
            threat_types=[m["threatType"] for m in threats],
            details=details
        )
