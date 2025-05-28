from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config.settings import get_settings, Settings
from src.routers import api_v1_router
from src.websockets import api_v1_websocket

settings: Settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> CORSMiddleware:

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
        docs_url="/docs",  # Standard docs URL
        redoc_url="/redoc",  # Standard ReDoc URL
        openapi_url=f"{settings.API_V1_STR}/openapi.json",  # OpenAPI schema URL
        lifespan=lifespan,  # Use the lifespan context manager
    )

    app.include_router(api_v1_router, prefix=settings.API_V1_STR)
    app.include_router(
        api_v1_websocket, prefix=settings.API_V1_STR + "/ws"
    )  # Example prefix

    @app.get("/health", tags=["Health Check"])
    async def health_check():
        return {"status": "ok"}

    return CORSMiddleware(
        app=app,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
