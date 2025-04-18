from abc import ABC, abstractmethod

from fastapi import BackgroundTasks

from app.schemas.shortener_schemas import URLStatsResponse, ClickEvent
from shared_models.kafka.url_validation import UrlValidationResult


class AbstractShortenerService(ABC):
    """ Abstract class for url shortener service """

    @abstractmethod
    async def create_short_url(self, long_url: str, background_tasks: BackgroundTasks) -> str:
        """ Create a short url """
        pass

    @abstractmethod
    async def update_validation_status(self, url_validation_result: UrlValidationResult) -> None:
        """ Update the validation status """
        pass

    @abstractmethod
    async def get_original_url(self, short_code: str) -> str:
        """ Get the original url """
        pass

    async def send_click_event(self, event: ClickEvent):
        """ Send click event to RabbitMQ for analytics """
        pass

    @abstractmethod
    async def get_stats(self, short_code: str) -> URLStatsResponse:
        """ Get the stats of the short url """
        pass

    @abstractmethod
    async def delete_short_url(self, short_code: str) -> bool:
        """ Delete the short url """
        pass

