from starlette.responses import RedirectResponse

from app.models.models import ShortenedURL
from app.schemas.shortener_schemas import ShortenResponse, URLStatsResponse


class ShortenerMapper:
    @staticmethod
    def to_short_response(url: ShortenedURL, base_url: str) -> ShortenResponse:
        return ShortenResponse(
            short_code=url.short_code,
            short_url=f"{base_url}/go/{url.short_code}",
        )

    @staticmethod
    def to_redirect_response(url: str) -> RedirectResponse:
        return RedirectResponse(
            url=url,
        )

    @staticmethod
    def to_url_stats_response(url: ShortenedURL) -> URLStatsResponse:
        return URLStatsResponse(
            short_code=url.short_code,
            clicks=url.clicks,
        )