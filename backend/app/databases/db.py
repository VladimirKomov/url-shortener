from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from app.configs.config import config

# Create engine
engine = create_async_engine(config.DATABASE_URL, echo=config.DEBUG)

# Create session factory
SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)


# Base class for models
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Dependency function for FastAPI routes
async def get_db():
    async with SessionLocal() as session:
        yield session
