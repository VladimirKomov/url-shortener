import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URL: str = os.getenv("MONGO_URL")
    KAFKA_URL: str = os.getenv("KAFKA_URL")
    KAFKA_TOPIC_URL_VALIDATION: str = os.getenv("KAFKA_TOPIC_URL_VALIDATION")
    KAFKA_GROUP_ID: str = os.getenv("KAFKA_GROUP_ID")

config = Config()