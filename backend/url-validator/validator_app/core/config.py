import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URL: str = os.getenv("MONGO_URL")

config = Config()