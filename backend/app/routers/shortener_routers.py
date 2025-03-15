from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.db import get_db
from app.schemas.shortener_schemas import ShortenRequest, ShortenResponse
from app.services.shortener_services import ShortenerServices

router = APIRouter()


@router.post("/shorter", response_model=ShortenResponse)
async def shorten_url(request: ShortenRequest, db: AsyncSession = Depends(get_db)):
    """Shorten url"""
    shortener_services = ShortenerServices(db)
    return await shortener_services.create_short_url(str(request.long_url))


@router.get("/s/{short_code}")
async def get_original_url(short_code: str, db: AsyncSession = Depends(get_db)):
    """Get original url"""
    shortener_services = ShortenerServices(db)
    return await shortener_services.get_original_url(short_code)


@router.get("/stats/{short_code}")
async def get_stats(short_code: str, db: AsyncSession = Depends(get_db)):
    """Increment clicks"""
    shortener_services = ShortenerServices(db)
    return await shortener_services.get_stats(short_code)


@router.delete("/s/{short_code}")
async def delete_short_url(short_code: str, db: AsyncSession = Depends(get_db)):
    """Delete short url"""
    shortener_services = ShortenerServices(db)
    success = await shortener_services.delete_short_url(short_code)
    return {"message": "Short URL deleted"}
