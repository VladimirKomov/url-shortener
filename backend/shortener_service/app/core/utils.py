import asyncio
import random
from typing import Callable, Coroutine, Any

from app.core.logger import logger


async def retry_connect(
        connect_func: Callable[[], Coroutine[Any, Any, bool | None]],
        *,
        retries: int = 5,
        base_delay: float = 2.0,
        name: str = "Service",
        raise_on_failure: bool = True
) -> None:
    """Retry wrapper for async connection functions.
    - `connect_func` may raise or return False.
    - If `raise_on_failure` is False, fail silently after all retries.
    """
    for attempt in range(1, retries + 1):
        try:
            result = await connect_func()
            if result is False:
                raise RuntimeError("Returned False from connect_func")

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
                msg = f"[{name}] All {retries} attempts failed."
                if raise_on_failure:
                    logger.critical(msg)
                    raise RuntimeError(f"Failed to connect to {name}")
                else:
                    logger.warning(f"{msg} Continuing without {name}.")
                    return
