import json

import aio_pika
from aio_pika.abc import AbstractRobustConnection

from app.core.config import config
from app.core.logger import logger
from app.messaging.rabbit_producer import rabbit_mq_producer_client
from app.schemas.shortener_schemas import ClickEvent


class ShortenerRabbitProducerServices:

    def __init__(self):
        self.client: AbstractRobustConnection | None = None
        self._queue_name = config.RABBITMQ_QUEUE_CLICK_EVENTS

    async def _get_client(self) -> AbstractRobustConnection:
        if self.client is None:
            self.client = await rabbit_mq_producer_client.get_client()
        return self.client

    async def send_click_event(self, event: ClickEvent) -> bool:
        """Send click event to RabbitMQ"""
        try:
            client = await self._get_client()
            channel = await client.channel()

            # Create a channel
            await channel.declare_queue(self._queue_name, durable=True)

            # Prepare a message
            payload = aio_pika.Message(
                body=json.dumps(event.model_dump(), default=str).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )

            # Publish
            await channel.default_exchange.publish(
                payload,
                routing_key=self._queue_name
            )

            logger.info(f"RabbitMQ event sent: short_code={event.short_code}")
            # Close the channel
            await channel.close()
            return True

        except Exception as e:
            logger.error(f"RabbitMQ send failed: {e}")
            return False
