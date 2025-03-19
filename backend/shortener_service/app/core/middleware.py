import time
from fastapi import Request
from app.core.logger import logger


async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url} {response.status_code} {process_time:.4f}s")
    return response
