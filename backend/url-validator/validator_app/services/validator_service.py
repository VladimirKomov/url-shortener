from shared_models.kafka.url_validation import UrlValidationKafkaMessage
from shared_models.kafka.url_validation import UrlValidationResult
from validator_app.mappers.validation_kafka_mapper import KafkaMapper
from validator_app.repositories.url_validation_repository import UrlValidationRepository
from validator_app.services.helpers.validation_google_service import GoogleUrlChecker
from validator_app.services.helpers.validation_kafka_producer_services import ValidationResultProducerService


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
        return KafkaMapper.to_kafka_response(
            payload,
            is_safe,
            threats,
            details
        )
