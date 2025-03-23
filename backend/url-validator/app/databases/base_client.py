import abc
import asyncio
from abc import ABC
from typing import Union

import redis.asyncio as aioredis
from aiokafka import AIOKafkaProducer

from app.core.logger import logger

ClientType = Union[AIOKafkaProducer, aioredis.Redis, None]


class BaseAsyncClient(ABC):
    _instance = None
    _lock = asyncio.Lock()
    client: ClientType

    def __new__(cls):
        """ Singleton pattern to connection """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = None
        return cls._instance

    @abc.abstractmethod
    async def _create_client(self) -> None:
        """ Create a client """
        pass

    @abc.abstractmethod
    async def _ping(self) -> bool:
        """ Check if the connection is alive """
        pass

    async def connect(self) -> None:
        """ Initialize connection if not already connected or lost """
        if self.client is None:
            await self._create_client()
        else:
            try:
                if not await self._ping():
                    raise ConnectionError("Ping failed")
            except Exception as e:
                logger.error(f"{self.__class__.__name__} connection error: {e}. Reconnecting...")
                await self._close_client()
                await self._create_client()

    async def get_client(self) -> ClientType:
        """ Get the client """
        await self.connect()
        if self.client is None:
            raise ConnectionError(f"{self.__class__.__name__} is not available!")
        return self.client

    @abc.abstractmethod
    async def _close_client(self) -> None:
        """ Close the connection """
        pass
