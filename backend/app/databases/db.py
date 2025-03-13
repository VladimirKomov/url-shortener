from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.configs.config import config

# Create engine
engine = create_async_engine(config.DATABASE_URL, echo=config.DEBUG)

# Create session factory
SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Dependency function for FastAPI routes
async def get_db():
    async with SessionLocal() as session:
        yield session