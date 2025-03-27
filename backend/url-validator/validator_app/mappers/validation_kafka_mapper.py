from datetime import datetime

from shared_models.kafka.url_validation import UrlValidationKafkaMessage, UrlValidationResult


class KafkaMapper:
    @staticmethod
    def to_kafka_response(
            payload: UrlValidationKafkaMessage,
            is_safe: bool | None,
            threats: list,
            details: str
    ) -> UrlValidationResult:
        return UrlValidationResult(
            short_code=payload.short_code,
            original_url=str(payload.original_url),
            # None - the check was not performed
            is_safe=is_safe,
            checked_at=datetime.now(),
            threat_types=[m["threatType"] for m in threats],
            details=details
        )
