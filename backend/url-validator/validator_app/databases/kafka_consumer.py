import asyncio
import json

from aiokafka import AIOKafkaConsumer
from aiokafka.structs import ConsumerRecord

from validator_app.core.config import config
from validator_app.core.logger import logger
from validator_app.databases.base_client import BaseAsyncClient
from validator_app.schemas.kafka_schemas import UrlValidationKafkaMessage


class KafkaConsumerClient(BaseAsyncClient):
    """Kafka Consumer Client"""

    def __init__(self):
        super().__init__()
        self._task = None
        self._running = False

    async def _ping(self) -> bool:
        """Kafka does not support ping — always return True"""
        return True

    async def _create_client(self) -> None:
        """Create Kafka Consumer"""
        if self.client is not None:
            return

        try:
            self.client = AIOKafkaConsumer(
                config.KAFKA_TOPIC_URL_VALIDATION,
                bootstrap_servers=config.KAFKA_URL,
                group_id=config.KAFKA_GROUP_ID,
                enable_auto_commit=False,
                auto_offset_reset="latest",
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            )
            await self.client.start()
            logger.info("Kafka consumer created and started")
        except Exception as e:
            logger.error(f"Error creating Kafka consumer: {e}")
            self.client = None

    async def _close_client(self):
        """Stop Kafka Consumer"""
        if self.client:
            try:
                await self.client.stop()
                logger.info("Kafka consumer stopped")
            except Exception as e:
                logger.error(f"Error stopping Kafka consumer: {e}")
            finally:
                self.client = None

    async def start_listening(self):
        """Running a Kafka listening Kafka"""
        if self._task or self._running:
            return
        await self._create_client()
        self._running = True
        self._task = asyncio.create_task(self._consume_loop())

    async def _consume_loop(self):
        """Asynchronous message processing cycle"""
        try:
            async for msg in self.client:
                await self._handle_message(msg)
        except asyncio.CancelledError:
            logger.info("Kafka consumer loop cancelled")
        except Exception as e:
            logger.error(f"Kafka consumer error: {e}")
        finally:
            self._running = False
            await self._close_client()

    async def _handle_message(self, msg: ConsumerRecord):
        """Processing a single message"""
        logger.info(f"Message received: {msg.value}")
        try:
            payload = UrlValidationKafkaMessage(**msg.value)
            logger.info(f"Received URL to validate: {payload.model_dump}")
            await self.client.commit()
            logger.info("Offset committed")
        except Exception as e:
            logger.error(f"Error handling message: {e}")

    async def shutdown(self):
        """Interrupting a background task"""
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                logger.info("Kafka consumer task cancelled")
            self._task = None
        await self._close_client()


kafka_consumer_client = KafkaConsumerClient()
