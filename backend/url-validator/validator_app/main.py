import asyncio

from validator_app.core.lifespan import lifespan_start, lifespan_shutdown


async def main():
    await lifespan_start()
    try:
        # wait indefinitely until Ctrl+C is interrupted
        await asyncio.Event().wait()
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("Shutdown signal received.")
    finally:
        await lifespan_shutdown()
        print("Shutdown complete.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("KeyboardInterrupt – stopping...")
