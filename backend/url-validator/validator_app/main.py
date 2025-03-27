import asyncio
from validator_app.core.bootstrap import app_container

stop_event = asyncio.Event()

async def main():
    # launching the container
    await app_container.init()
    try:
        # stopping main before calling stop_event.set()
        await stop_event.wait()
    except KeyboardInterrupt:
        print("KeyboardInterrupt received")
    except asyncio.CancelledError:
        pass
    finally:
        await app_container.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
