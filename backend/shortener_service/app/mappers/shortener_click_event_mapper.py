from datetime import datetime

from fastapi import Request

from app.schemas.shortener_schemas import ClickEvent


class ClickEventMapper:
    @staticmethod
    def from_request(short_code: str, request: Request) -> ClickEvent:
        return ClickEvent(
            short_code=short_code,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            referer=request.headers.get("referer"),
            timestamp=datetime.now()
        )
