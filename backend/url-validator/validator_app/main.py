import asyncio
import sys

from validator_app.core.bootstrap import app_container
from validator_app.core.logger import logger

stop_event = asyncio.Event()

async def main():
    # launching the container
    try:
        await app_container.init()
    except Exception as e:
        # critical error at startup
        logger.critical(f"Critical error during startup: {e}")
        sys.exit(1)
    try:
        # stopping main before calling stop_event.set()
        await stop_event.wait()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received")
    except asyncio.CancelledError:
        pass
    finally:
        await app_container.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
