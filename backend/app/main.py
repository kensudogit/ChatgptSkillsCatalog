import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.config import get_settings
from app.database import SessionLocal, init_models
from app.schemas import HealthResponse
from app.services.sample_seed import seed_sample_skills
from app.services.storage import StorageService


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    # Create tables (for MVP; use Alembic migrations in production hardening)
    init_models()
    StorageService(settings).ensure_dirs()
    Path(settings.git_workdir).mkdir(parents=True, exist_ok=True)
    db = SessionLocal()
    try:
        seed_sample_skills(db, settings)
    except Exception:  # pragma: no cover - never block startup on seed
        logging.getLogger(__name__).exception("Sample skill seed failed")
    finally:
        db.close()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    # uvicorn only configures its own loggers, so attach a root handler to keep
    # application logs in the container output.
    logging.basicConfig(
        level=logging.DEBUG if settings.debug else logging.INFO,
        format="%(levelname)s:     %(name)s - %(message)s",
    )
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
