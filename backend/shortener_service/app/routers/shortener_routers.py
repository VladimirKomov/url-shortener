from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.params import Depends
from starlette.responses import RedirectResponse

from app.dependencies.shortener_service import get_url_shortener_service
from app.interfaces.shortener_interfaces import AbstractShortenerService
from app.mappers.shortener_click_event_mapper import ClickEventMapper
from app.mappers.shortener_mapper import ShortenerMapper
from app.schemas.shortener_schemas import ShortenRequest, ShortenResponse, URLStatsResponse, ClickEvent

router = APIRouter()


@router.post("/shorter", response_model=ShortenResponse)
async def shorten_url(
        request: ShortenRequest,
        background_tasks: BackgroundTasks,
        service: AbstractShortenerService = Depends(get_url_shortener_service)
):
    """Shorten url"""
    return await service.create_short_url(str(request.long_url), background_tasks)


@router.get("/go/{short_code}", response_class=RedirectResponse)
async def get_original_url(
        short_code: str,
        request: Request,
        background_tasks: BackgroundTasks,
        service: AbstractShortenerService = Depends(get_url_shortener_service)
):
    """ Redirect to original url """
    original_url = await service.get_original_url(
        short_code=short_code,
    )
    # send_click_event to statistics
    event: ClickEvent = ClickEventMapper.from_request(short_code, request)
    background_tasks.add_task(service.send_click_event, event)

    return ShortenerMapper.to_redirect_response(original_url)


@router.get("/stats/{short_code}", response_model=URLStatsResponse)
async def get_stats(
        short_code: str,
        service: AbstractShortenerService = Depends(get_url_shortener_service)
):
    """Increment clicks"""
    return await service.get_stats(short_code)


@router.delete("/go/{short_code}")
async def delete_short_url(
        short_code: str,
        service: AbstractShortenerService = Depends(get_url_shortener_service)
):
    """Delete short url"""
    success = await service.delete_short_url(short_code)
    if not success:
        return {"message": "URL not found"}
    return {"message": "Short URL deleted"}
