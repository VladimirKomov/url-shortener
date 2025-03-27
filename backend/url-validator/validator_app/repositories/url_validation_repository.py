from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from validator_app.core.config import config
from shared_models.kafka.url_validation import UrlValidationResult


class UrlValidationRepository:
    def __init__(self, client: AsyncIOMotorClient):
        db = client[config.MONGO_DB_NAME]
        self.collection = db[config.MONGO_COLLECTION_NAME]

    async def save(self, result: UrlValidationResult):
        doc = result.model_dump()
        doc["inserted_at"] = datetime.now()
        await self.collection.insert_one(doc)


