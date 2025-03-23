from motor.motor_asyncio import AsyncIOMotorClient

from validator_app.core.logger import logger
from validator_app.databases.base_client import BaseAsyncClient


class MongoDBClient(BaseAsyncClient):

    async def _ping(self) -> bool:
        """ Check connection """
        try:
            return await self.client.admin.command('ping')
        except Exception:
            return False

    async def _create_client(self) -> AsyncIOMotorClient:
        """ Returns the MongoDB client """
        await self.connect()
        return self.client

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
