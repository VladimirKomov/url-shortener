import json

import aiokafka

from validator_app.core.base_client import BaseAsyncClient
from validator_app.core.config import config
from validator_app.core.logger import logger


class KafkaProducerClient(BaseAsyncClient):
    """ Kafka Producer Client """

    async def _ping(self) -> bool:
        """ Kafka does not support ping, so always return True """
        return True

    async def _create_client(self) -> None:
        """ Create Kafka Producer """
        async with self._lock:
            if self.client is None:
                try:
                    self.client = aiokafka.AIOKafkaProducer(
                        bootstrap_servers=config.KAFKA_URL,
                        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                    )
                    await self.client.start()
                    logger.info("Kafka client created")
                except Exception as e:
                    logger.error(f"Error creating Kafka client: {e}")
                    self.client = None
                    raise

    async def _close_client(self):
        """ Close the Kafka connection """
        if self.client:
            try:
                await self.client.stop()
                logger.info("Kafka producer closed")
            except Exception as e:
                logger.error(f"Error closing Kafka producer: {e}")
            finally:
                self.client = None


# Global Kafka client instance
kafka_producer_client = KafkaProducerClient()
