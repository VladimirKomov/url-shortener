from aiokafka import AIOKafkaProducer

from shared_models.kafka.url_validation import UrlValidationResult
from validator_app.core.config import config
from validator_app.core.logger import logger
from validator_app.messaging.kafka_producer import kafka_producer_client


class ValidationResultProducerService:
    def __init__(self):
        self._client: AIOKafkaProducer | None = None

    async def _get_client(self) -> AIOKafkaProducer:
        if self._client is None:
            self._client = await kafka_producer_client.get_client()
        return self._client

    async def send_url_validation_result(self, result: UrlValidationResult) -> bool:
        """Send URL to Kafka for async validation"""
        client = await self._get_client()

        try:
            await client.send_and_wait(config.KAFKA_TOPIC_VALIDATION_RESULT, result.model_dump())
            logger.info(f"Sent to Kafka: {result.model_dump()}")
            return True
        except Exception as e:
            logger.error(f"Kafka send failed: {e}")
            return False
