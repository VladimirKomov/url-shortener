from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl

class ShortenRequest(BaseModel):
    long_url: HttpUrl

class ShortenResponse(BaseModel):
    short_code: str
    short_url: str

class URLStatsResponse(BaseModel):
    short_code: str
    clicks: int

class ClickEvent(BaseModel):
    short_code: str
    ip_address: str
    user_agent: Optional[str]
    referer: Optional[str]
    timestamp: datetime
