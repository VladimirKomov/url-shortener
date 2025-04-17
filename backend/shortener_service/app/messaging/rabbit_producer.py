import aio_pika

from app.core.base_client import BaseAsyncClient
from app.core.config import config


class RabbitMQProducerClient(BaseAsyncClient):
    """ RabbitMQ Producer Client """

    async def _ping(self) -> bool:
        """ RabbitMQ simple channel """
        try:
            channel = await self.client.channel()
            await channel.close()
            return True
        except Exception:
            return False

    async def _create_client(self) -> None:
        """ Create RabbitMQ Client """
        self.client = await aio_pika.connect_robust(
            host=config.RABBITMQ_HOST,
            port=config.RABBITMQ_PORT,
            login=config.RABBITMQ_DEFAULT_USER,
            password=config.RABBITMQ_DEFAULT_PASS,
            virtualhost=config.RABBITMQ_VHOST
        )

    async def _close_client(self) -> None:
        """ Close RabbitMQ Client """
        if self.client:
            await self.client.close()

rabbit_mq_producer_client = RabbitMQProducerClient()