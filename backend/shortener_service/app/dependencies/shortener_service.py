from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.postgresql import get_db, SessionLocal
from app.interfaces.shortener_interfaces import AbstractShortenerService
from app.services.postgres_shortener_service import PostgresShortenerService

# for FastAPI routers
def get_url_shortener_service(
        db: AsyncSession = Depends(get_db)
) -> AbstractShortenerService:
    return PostgresShortenerService(db)

# for Kafka consumer
async def create_url_shortener_service() -> AbstractShortenerService:
    async with SessionLocal() as session:
        return PostgresShortenerService(session)