from fastapi import APIRouter, BackgroundTasks
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.databases.postgresql import get_db
from app.databases.redis import redis_client
from app.mappers.shortener_mapper import ShortenerMapper
from app.schemas.shortener_schemas import ShortenRequest, ShortenResponse, URLStatsResponse
from app.services.shortener_services import ShortenerServices

router = APIRouter()


@router.post("/shorter", response_model=ShortenResponse)
async def shorten_url(request: ShortenRequest, db: AsyncSession = Depends(get_db)):
    """Shorten url"""
    shortener_services = ShortenerServices(db)
    return await shortener_services.create_short_url(str(request.long_url))


@router.get("/go/{short_code}", response_class=RedirectResponse)
async def get_original_url(
        short_code: str,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_db)
):
    """Redirect to original url"""
    shortener_services = ShortenerServices(db)
    original_url = await shortener_services.get_original_url(
        short_code=short_code,
        background_tasks=background_tasks
    )
    return ShortenerMapper.to_redirect_response(original_url)


@router.get("/stats/{short_code}", response_model=URLStatsResponse)
async def get_stats(short_code: str, db: AsyncSession = Depends(get_db)):
    """Increment clicks"""
    shortener_services = ShortenerServices(db)
    return await shortener_services.get_stats(short_code)


@router.delete("/go/{short_code}")
async def delete_short_url(short_code: str, db: AsyncSession = Depends(get_db)):
    """Delete short url"""
    shortener_services = ShortenerServices(db)
    success = await shortener_services.delete_short_url(short_code)
    if not success:
        return {"message": "URL not found"}
    return {"message": "Short URL deleted"}

# for test, delete after
@router.get("/test-redis/")
async def test_redis():
    client = await redis_client.get_client()
    await client.set("test_key", "Hello, Redis!", ex=60)
    value = await client.get("test_key")
    return {"test_key": value}
