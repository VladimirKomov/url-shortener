from pydantic import BaseModel, HttpUrl

class URLValidationMessage(BaseModel):
    original_url: HttpUrl
    short_code: str
