from pydantic import BaseModel, HttpUrl

class ShortenRequest(BaseModel):
    long_url: HttpUrl

class ShortenResponse(BaseModel):
    short_code: str
    short_url: str

class URLStats(BaseModel):
    short_code: str
    clicks: int
