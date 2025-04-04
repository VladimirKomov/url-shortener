import asyncio
import random
from typing import Callable

from validator_app.core.logger import logger


async def retry_connect(
        connect_func: Callable,
        *,
        retries: int = 5,
        base_delay: float = 2.0,
        name: str = "Service"
) -> None:
    """Retry wrapper for async connection functions"""
    for attempt in range(1, retries + 1):
        try:
            await connect_func()
            logger.info(f"{name} connected successfully")
            return
        except Exception as e:
            delay = base_delay * (2 ** (attempt - 1))
            jitter = random.uniform(0, delay)
            wait_time = delay + jitter
            logger.warning(f"[{name}] Attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                await asyncio.sleep(wait_time)
            else:
                logger.critical(f"[{name}] All {retries} attempts failed.")
                raise RuntimeError(f"Failed to connect to {name}")
