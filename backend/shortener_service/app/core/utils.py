import asyncio
from typing import Callable

from app.core.logger import logger


async def retry_connect(
        connect_func: Callable,
        *,
        retries: int = 5,
        delay: float = 2.0,
        name: str = "Service"
):
    """Retry wrapper for async connection functions"""
    for attempt in range(1, retries + 1):
        try:
            await connect_func()
            logger.info(f"{name} connected successfully")
            return
        except Exception as e:
            logger.warning(f"[{name}] Attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                await asyncio.sleep(delay)
            else:
                logger.critical(f"[{name}] All {retries} attempts failed.")
                raise RuntimeError(f"Failed to connect to {name}")