from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logger import logger
from app.core.utils import retry_connect
from app.databases.redis import redis_client
from app.messaging.rabbit_producer import rabbit_mq_producer_client
from app.messaging.kafka_consumer import kafka_consumer_client
from app.messaging.kafka_producer import kafka_producer_client


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Connect to Redis and Kafka before starting the server and close them after"""
    try:
        # Redis not critical, responsible for cache, just logging
        await retry_connect(redis_client.safe_connect, name="Redis")
    except Exception as e:
        logger.warning(f"Redis unavailable, continuing without cache: {e}")
    try:
        # Try to create connections, if impossible, we call an error and stop the application
        await retry_connect(kafka_producer_client.strict_connect, name="Kafka Producer")
        await retry_connect(kafka_consumer_client.start_listening, name="Kafka Consumer")
        await retry_connect(rabbit_mq_producer_client.strict_connect, name="RabbitMQ Producer")
    except Exception as e:
        logger.critical(f"Startup failed: {e}")
        raise e
    yield
    await redis_client.close()
    await kafka_producer_client.close()
    await kafka_consumer_client.shutdown()
    await rabbit_mq_producer_client.close()
