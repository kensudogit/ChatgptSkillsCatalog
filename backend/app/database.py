import logging
import time
from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def describe_target() -> str:
    """Connection target without credentials, safe to write to logs."""
    url = make_url(settings.database_url)
    return f"{url.host}:{url.port or 5432}/{url.database}"


def ensure_indexes() -> None:
    """Create helpful indexes on existing databases (create_all won't alter)."""
    statements = [
        "CREATE INDEX IF NOT EXISTS ix_skills_updated_at ON skills (updated_at)",
        "CREATE INDEX IF NOT EXISTS ix_skills_source_type ON skills (source_type)",
        "CREATE INDEX IF NOT EXISTS ix_skills_git_source_path ON skills (git_source_id, git_path)",
        "CREATE INDEX IF NOT EXISTS ix_skill_tags_tag ON skill_tags (tag)",
    ]
    with engine.begin() as conn:
        for stmt in statements:
            try:
                conn.execute(text(stmt))
            except Exception as exc:  # pragma: no cover - dialect differences
                logger.warning("Index ensure skipped (%s): %s", stmt, exc)


def init_models(retries: int = 5, delay_sec: float = 2.0) -> None:
    """Create tables, tolerating a database that is still booting.

    Managed databases are often reachable a few seconds after the app starts,
    so a transient failure here should not kill the container.
    """
    target = describe_target()
    for attempt in range(1, retries + 1):
        try:
            Base.metadata.create_all(bind=engine)
            ensure_indexes()
            logger.info("Database ready at %s", target)
            return
        except OperationalError as exc:
            if attempt == retries:
                logger.error(
                    "Cannot reach database at %s after %s attempts. "
                    "Set DATABASE_URL to your managed database URL.",
                    target,
                    retries,
                )
                raise
            logger.warning(
                "Database at %s not ready (attempt %s/%s): %s",
                target,
                attempt,
                retries,
                exc.orig or exc,
            )
            time.sleep(delay_sec * attempt)
