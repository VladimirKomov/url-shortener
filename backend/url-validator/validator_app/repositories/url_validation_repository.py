from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from validator_app.core.config import config
from validator_app.services.validator_service import UrlValidationResult


class UrlValidationRepository:
    def __init__(self, client: AsyncIOMotorClient):
        db = client[config.MONGO_DB_NAME]
        self.collection = db[config.MONGO_COLLECTION_NAME]

    async def save(self, result: UrlValidationResult):
        doc = result.model_dump()
        doc["inserted_at"] = datetime.utcnow()
        await self.collection.insert_one(doc)


