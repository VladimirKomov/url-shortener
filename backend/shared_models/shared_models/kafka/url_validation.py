from pydantic import BaseModel, HttpUrl


class UrlValidationKafkaMessage(BaseModel):
    original_url: HttpUrl
    short_code: str
