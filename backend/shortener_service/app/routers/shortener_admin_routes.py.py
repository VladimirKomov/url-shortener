from fastapi import APIRouter, HTTPException

from app.core.logger import logger
from app.schemas.kafka_schemas import URLValidationMessage
from app.services.helpers.shortener_kafka_producer_services import ShortenerKafkaProducerService

router = APIRouter()
kafka_service = ShortenerKafkaProducerService()


@router.post("/admin/resend-validation", include_in_schema=True, tags=["admin"])
async def resend_url_validation(data: URLValidationMessage):
    """
    Admin endpoint to manually resend a URL for validation via Kafka.

    This can be used in cases where the original validation failed,
    got stuck, or needs to be retried manually for specific short links.
    """
    success = await kafka_service.send_url_validation(
        original_url=str(data.original_url),
        short_code=data.short_code,
    )
    if not success:
        logger.error(f"Failed to resend validation for short_code={data.short_code}, url={data.original_url}")
        raise HTTPException(status_code=500, detail="Failed to send message to Kafka")

    return {"status": "ok" if success else "failed"}

