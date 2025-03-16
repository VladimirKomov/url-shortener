import uvicorn
from fastapi import FastAPI
from app.routers import shortener_routers

app = FastAPI(
    title="URL Shortener API",
    description="API для сокращения ссылок",
    version="1.0.0"
)

app.include_router(shortener_routers.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

