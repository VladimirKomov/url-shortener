import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URL: str = os.getenv("MONGO_URL")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "url_validator")
    MONGO_COLLECTION_NAME: str = os.getenv("MONGO_COLLECTION_NAME")

    KAFKA_URL: str = os.getenv("KAFKA_URL")
    KAFKA_TOPIC_URL_VALIDATION: str = os.getenv("KAFKA_TOPIC_URL_VALIDATION")
    KAFKA_GROUP_ID: str = os.getenv("KAFKA_GROUP_ID")

    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")

config = Config()