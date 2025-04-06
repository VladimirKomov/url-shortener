from motor.motor_asyncio import AsyncIOMotorClient

from validator_app.core.config import Config
from validator_app.core.logger import logger
from validator_app.core.base_client import BaseAsyncClient


class MongoDBClient(BaseAsyncClient):

    async def _ping(self) -> bool:
        """ Check connection """
        try:
            result = await self.client.admin.command('ping')
            logger.debug(f"Ping result: {result}")
            return result.get("ok") == 1.0
        except Exception as e:
            logger.warning(f"Ping failed with error: {e}")
            return False

    async def _create_client(self) -> None:
        """ Returns the MongoDB client """
        async with self._lock:
            if self.client is None:
                try:
                    self.client = AsyncIOMotorClient(
                        Config.MONGO_URL,
                        serverSelectionTimeoutMS=3000,
                        retryWrites=False
                    )
                    logger.info("MongoDB client created")
                except Exception as e:
                    logger.error(f"Error creating MongoDB client: {e}")
                    self.client = None
                    raise

    async def _close_client(self) -> None:
        """ Close the MongoDB connection """
        if self.client:
            try:
                self.client.close()
                logger.info("MongoDB connection closed")
            except Exception as e:
                logger.error(f"Error closing MongoDB connection: {e}")
            finally:
                self.client = None


mongodb_client = MongoDBClient()
