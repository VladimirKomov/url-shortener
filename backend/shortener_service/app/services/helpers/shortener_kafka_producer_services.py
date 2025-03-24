from aiokafka import AIOKafkaProducer

from app.core.config import config
from app.core.logger import logger
from app.databases.kafka import kafka_producer_client
from app.mappers.validation_kafka_mapper import ValidationKafkaMapper


class ShortenerKafkaProducerService:
    def __init__(self):
        self._client: AIOKafkaProducer | None = None

    async def _get_client(self) -> AIOKafkaProducer:
        if self._client is None:
            self._client = await kafka_producer_client.get_client()
        return self._client

    async def send_url_validation(self, short_code: str, original_url: str) -> bool:
        """Send URL to Kafka for async validation"""
        client = await self._get_client()
        payload = ValidationKafkaMapper.to_kafka_message(
            short_code=short_code,
            original_url=original_url,
        )
        try:
            await client.send_and_wait(config.KAFKA_TOPIC_URL_VALIDATION, payload.model_dump())
            logger.info(f"Sent to Kafka: {payload.model_dump()}")
            return True
        except Exception as e:
            logger.error(f"Kafka send failed: {e}")
            return False
