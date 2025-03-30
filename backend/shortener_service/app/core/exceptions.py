import traceback

from fastapi import HTTPException, Request
from starlette.responses import JSONResponse

from app.core.logger import logger


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    error_traceback = traceback.format_exc()
    logger.error(
        f"HTTP Error: {request.method} {request.url} - {str(exc)}\n{error_traceback}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    error_traceback = traceback.format_exc()
    logger.error(
        f"Unhandled Error: {request.method} {request.url} - {str(exc)}\n{error_traceback}"
    )
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )


class URLNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Short URL not found")


class URLInvalidException(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="This URL was marked as unsafe")


class URLPendingException(HTTPException):
    def __init__(self):
        super().__init__(status_code=425, detail="This URL is still being validated")


class URLAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="This URL is already shortened")
