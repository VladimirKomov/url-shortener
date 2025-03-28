from datetime import datetime

from shared_models.kafka.enums import ValidationStatus
from shared_models.kafka.url_validation import UrlValidationKafkaMessage, UrlValidationResult


class KafkaMapper:
    @staticmethod
    def to_kafka_response(
            payload: UrlValidationKafkaMessage,
            is_safe: bool | None,
            threats: list,
            details: str
    ) -> UrlValidationResult:

        if is_safe is True:
            validation_status = ValidationStatus.VALID
        elif is_safe is False:
            validation_status = ValidationStatus.INVALID
        else:
            validation_status = ValidationStatus.PENDING

        return UrlValidationResult(
            short_code=payload.short_code,
            original_url=str(payload.original_url),
            validation_status=validation_status,
            checked_at=datetime.now(),
            threat_types=[m["threatType"] for m in threats],
            details=details
        )
