import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URI: str = os.getenv("DATABASE_URI")
    DEBUG: bool = os.getenv("DEBUG")

config = Config()