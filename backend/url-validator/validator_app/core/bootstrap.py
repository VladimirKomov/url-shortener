from validator_app.core.config import config
from validator_app.core.utils import retry_connect
from validator_app.repositories.url_validation_repository import UrlValidationRepository
from validator_app.services.helpers.validation_google_service import GoogleUrlChecker
from validator_app.services.helpers.validation_kafka_producer_services import ValidationResultProducerService
from validator_app.services.validator_service import ValidatorService
from validator_app.messaging.kafka_consumer import KafkaConsumerClient
from validator_app.messaging.kafka_producer import kafka_producer_client
from validator_app.databases.mongo_db import mongodb_client


class AppContainer:
    """Holds initialized services and clients."""

    def __init__(self):
        self.mongo_client = mongodb_client
        self.kafka_producer = kafka_producer_client

        self.mongo_repository: UrlValidationRepository | None = None
        self.google_service: GoogleUrlChecker | None = None
        self.kafka_result_producer: ValidationResultProducerService | None = None
        self.validator_service: ValidatorService | None = None
        self.kafka_consumer: KafkaConsumerClient | None = None

    async def init(self):
        # Low-level clients с retry
        await retry_connect(self.mongo_client.strict_connect(), name="MongoDB")
        await retry_connect(self.kafka_producer.strict_connect, name="Kafka Producer")

        # High-level components
        self.mongo_repository = UrlValidationRepository(self.mongo_client.client)
        self.google_service = GoogleUrlChecker(api_key=config.GOOGLE_API_KEY)
        self.kafka_result_producer = ValidationResultProducerService()

        # Compose validator service
        self.validator_service = ValidatorService(
            mongo_repository=self.mongo_repository,
            google_service=self.google_service,
            kafka_producer_service=self.kafka_result_producer,
        )

        self.kafka_consumer = KafkaConsumerClient(self.validator_service)
        await retry_connect(self.kafka_consumer.start_listening, name="Kafka Consumer")

    async def shutdown(self):
        if self.kafka_consumer:
            await self.kafka_consumer.shutdown()
        await self.kafka_producer.close()
        await self.mongo_client.close()


# global container
app_container = AppContainer()
