import json

import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractChannel, AbstractExchange

from app.core.config import config
from app.core.logger import logger
from app.messaging.rabbit_producer import rabbit_mq_producer_client
from app.schemas.shortener_schemas import ClickEvent


class ShortenerRabbitProducerServices:

    def __init__(self):
        self.client: AbstractRobustConnection | None = None
        self._channel: AbstractChannel | None = None
        self._exchange: AbstractExchange | None = None
        self._exchange_name = config.RABBITMQ_EXCHANGE_CLICKS
        self._routing_key = config.RABBITMQ_ROUTING_KEY_CLICKS

    async def _get_client(self) -> AbstractRobustConnection:
        if self.client is None:
            self.client = await rabbit_mq_producer_client.get_client()
        return self.client

    async def _get_channel(self) -> AbstractChannel:
        if self._channel is None or self._channel.is_closed:
            client = await self._get_client()
            self._channel = await client.channel()
        return self._channel

    async def _get_exchange(self) -> AbstractExchange:
        if self._exchange is None or getattr(self._exchange, "is_closed", True):
            channel = await self._get_channel()
            self._exchange = await channel.declare_exchange(
                name=self._exchange_name,
                type=aio_pika.ExchangeType.TOPIC,
                durable=True,
            )
        return self._exchange

    async def send_click_event(self, event: ClickEvent) -> bool:
        """Send click event to RabbitMQ"""
        try:
            # Announce exchange
            exchange = await self._get_exchange()

            # field 'pattern' is required for Nestjs
            message_body = {
                "pattern": self._routing_key,
                "data": event.model_dump(),
            }

            # Prepare a message
            payload = aio_pika.Message(
                #body=json.dumps(event.model_dump(), default=str).encode(),
                body=json.dumps(message_body, default=str).encode(),
                # save the message
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )

            # Publish
            await exchange.publish(
                payload,
                routing_key=self._routing_key,
                mandatory=True
            )

            logger.info(f"RabbitMQ event sent: short_code={event.short_code} for key={self._routing_key}")
            return True

        except Exception as e:
            logger.error(f"RabbitMQ send failed: {e}")
            return False
