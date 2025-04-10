import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "1")
    ALLOW_REDIRECT_IF_PENDING = os.getenv("ALLOW_REDIRECT_IF_PENDING", "false").lower() in ("true", "1")
    BASE_URL: str = os.getenv("BASE_URL")

    REDIS_URL: str = os.getenv("REDIS_URL")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")

    KAFKA_URL: str = os.getenv("KAFKA_URL")
    KAFKA_TOPIC_URL_VALIDATION: str = os.getenv("KAFKA_TOPIC_URL_VALIDATION")
    KAFKA_GROUP_ID: str = os.getenv("KAFKA_GROUP_ID")
    KAFKA_TOPIC_VALIDATION_RESULT: str = os.getenv("KAFKA_TOPIC_VALIDATION_RESULT")

config = Config()