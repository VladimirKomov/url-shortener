from app.models.models import ShortenedURL
from app.schemas.shortener_schemas import ShortenResponse


class ShortenerMapper:
    @staticmethod
    def to_short_response(url: ShortenedURL, base_url: str) -> ShortenResponse:
        return ShortenResponse(
            short_code=url.short_code,
            short_url=f"/{base_url}/{url.short_code}",
        )