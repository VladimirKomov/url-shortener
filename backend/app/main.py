import time
import traceback
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from starlette.responses import JSONResponse

from app.core.logger import logger
from app.databases.redis import redis_client
from app.routers import shortener_routers

@asynccontextmanager
async def lifespan(_: FastAPI):
    await redis_client.connect()
    yield
    await redis_client.close()

app = FastAPI(
    title="URL Shortener API",
    description="API for shortening links",
    version="1.0.0",
    lifespan=lifespan
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error_traceback = traceback.format_exc()
    logger.error(
        f"Error: {request.method} {request.url} - {str(exc)}\n{error_traceback}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    error_traceback = traceback.format_exc()
    logger.error(
        f"Error: {request.method} {request.url} - {str(exc)}\n{error_traceback}"
    )
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url} {response.status_code} {process_time:.4f}s")
    return response

app.include_router(shortener_routers.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

