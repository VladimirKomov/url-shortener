import asyncio
import json

from aiokafka import AIOKafkaConsumer
from aiokafka.structs import ConsumerRecord

from shared_models.kafka.url_validation import UrlValidationKafkaMessage
from validator_app.core.config import config
from validator_app.core.logger import logger
from validator_app.services.validator_service import ValidatorService


class KafkaConsumerClient:
    """Kafka Consumer Client for processing URL validation messages."""

    def __init__(self, validator_service: ValidatorService):
        """
        Initialize the KafkaConsumerClient with required dependencies.
        """
        self.validator_service = validator_service
        self.client: AIOKafkaConsumer | None = None
        self._task = None
        self._running = False

    async def start(self):
        """
        Create and start the Kafka consumer client.
        """
        if self.client is not None:
            return

        try:
            self.client = AIOKafkaConsumer(
                config.KAFKA_TOPIC_URL_VALIDATION,
                bootstrap_servers=config.KAFKA_URL,
                group_id=config.KAFKA_GROUP_ID,
                sasl_mechanism="PLAIN",
                sasl_plain_username=config.KAFKA_USERNAME,
                sasl_plain_password=config.KAFKA_PASSWORD,
                security_protocol="SASL_PLAINTEXT",
                enable_auto_commit=False,
                auto_offset_reset="latest",
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            )
            await self.client.start()
            logger.info("Kafka consumer created and started")
        except Exception as e:
            logger.error(f"Failed to create Kafka consumer: {e}")
            self.client = None

    async def stop(self):
        """
        Stop and clean up the Kafka consumer client.
        """
        if self.client:
            try:
                await self.client.stop()
                logger.info("Kafka consumer stopped")
            except Exception as e:
                logger.error(f"Error stopping Kafka consumer: {e}")
            finally:
                self.client = None

    async def start_listening(self):
        """
        Start listening to Kafka messages in a background task.
        """
        if self._task or self._running:
            return

        await self.start()
        self._running = True
        self._task = asyncio.create_task(self._consume_loop())

    async def _consume_loop(self):
        """
        Asynchronous loop that continuously consumes and handles Kafka messages.
        """
        try:
            async for msg in self.client:
                await self._handle_message(msg)
        except asyncio.CancelledError:
            logger.info("Kafka consumer loop cancelled")
        except Exception as e:
            logger.error(f"Kafka consumer error: {e}")
        finally:
            self._running = False
            await self.stop()

    async def _handle_message(self, msg: ConsumerRecord):
        """
        Handle a single Kafka message by parsing and processing it.
        """
        logger.info(f"Kafka message received: {msg.value}")
        try:
            payload = UrlValidationKafkaMessage(**msg.value)
            logger.info(f"Parsed payload: {payload.model_dump()}")
            await self.validator_service.handle_message(payload)
            await self.client.commit()
            logger.info("Kafka offset committed")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    async def shutdown(self):
        """
        Cancel the background task and shut down the consumer gracefully.
        """
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                logger.info("Kafka consumer task cancelled")
            self._task = None
        await self.stop()
