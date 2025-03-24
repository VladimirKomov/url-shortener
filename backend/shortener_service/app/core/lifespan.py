from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.databases.kafka import kafka_producer_client
from app.databases.redis import redis_client


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Connect to Redis and Kafka before starting the server and close them after"""
    await redis_client.connect()
    await kafka_producer_client.connect()
    yield
    await redis_client.close()
    await kafka_producer_client.close()