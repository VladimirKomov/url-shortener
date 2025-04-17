import aio_pika

from app.core.base_client import BaseAsyncClient
from app.core.config import config
from app.core.logger import logger


class RabbitMQProducerClient(BaseAsyncClient):
    """ RabbitMQ Producer Client """

    async def _ping(self) -> bool:
        """ RabbitMQ simple channel """
        try:
            channel = await self.client.channel()
            await channel.close()
            logger.debug("RabbitMQ simple channel closed")
            return True
        except Exception:
            logger.warning("RabbitMQ simple channel error")
            return False

    async def _create_client(self) -> None:
        """ Create RabbitMQ Client """
        async with self._lock:
            if self.client is None:
                try:
                    self.client = await aio_pika.connect_robust(
                        host=config.RABBITMQ_HOST,
                        port=config.RABBITMQ_PORT,
                        login=config.RABBITMQ_DEFAULT_USER,
                        password=config.RABBITMQ_DEFAULT_PASS,
                        virtualhost=config.RABBITMQ_VHOST
                    )
                except Exception as e:
                    logger.error(f"Error creating RabbitMQ client: {e}")
                    self.client = None
                    raise

    async def _close_client(self) -> None:
        """ Close RabbitMQ Client """
        if self.client:
            try:
                await self.client.close()
                logger.info("RabbitMQ client closed")
            except Exception as e:
                logger.error(f"Error closing RabbitMQ client: {e}")
            finally:
                self.client = None

# Global Rabbit client
rabbit_mq_producer_client = RabbitMQProducerClient()