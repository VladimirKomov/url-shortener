import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "1")

config = Config()