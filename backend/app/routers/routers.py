from sqlalchemy.ext.asyncio import AsyncSession


async def get_short_code(db: AsyncSession, short_code: str):
    return "short_code"