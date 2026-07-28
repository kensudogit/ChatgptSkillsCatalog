from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.config import get_settings
from app.database import Base, engine
from app.schemas import HealthResponse
from app.services.storage import StorageService


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    # Create tables (for MVP; use Alembic migrations in production hardening)
    Base.metadata.create_all(bind=engine)
    StorageService(settings).ensure_dirs()
    Path(settings.git_workdir).mkdir(parents=True, exist_ok=True)
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix=settings.api_prefix)

    @app.get("/health", response_model=HealthResponse, tags=["health"])
    def health():
        return HealthResponse(status="ok", app=settings.app_name)

    return app


app = create_app()
