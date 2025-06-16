from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger

from app.api.routes import router
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan (startup and shutdown events).
    """
    logger.info(f"Starting up {settings.APP_NAME}...")
    # You can add startup logic here, e.g., connecting to DB
    yield
    logger.info("Shutting down...")
    # You can add shutdown logic here


def create_app() -> FastAPI:
    """
    Create the FastAPI application.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        lifespan=lifespan,
    )
    app.include_router(router, prefix="/api")

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "ok"}

    return app


app = create_app()
