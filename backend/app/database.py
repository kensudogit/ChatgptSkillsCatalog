import logging
import time
from collections.abc import Generator

from sqlalchemy import create_engine
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


def init_models(retries: int = 5, delay_sec: float = 2.0) -> None:
    """Create tables, tolerating a database that is still booting.

    Managed databases are often reachable a few seconds after the app starts,
    so a transient failure here should not kill the container.
    """
    target = describe_target()
    for attempt in range(1, retries + 1):
        try:
            Base.metadata.create_all(bind=engine)
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
