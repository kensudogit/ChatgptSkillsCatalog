from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "ChatGPT Skills Catalog"
    api_prefix: str = "/api/v1"
    debug: bool = False

    database_url: str = "postgresql+psycopg2://skills:skills@db:5432/skills_catalog"

    upload_dir: str = "/app/uploads"
    max_upload_size_mb: int = 50
    max_zip_files: int = 200
    max_uncompressed_size_mb: int = 200
    max_compression_ratio: float = 100.0

    # Local filesystem by default; set STORAGE_BACKEND=s3 for ECS
    storage_backend: str = "local"
    s3_bucket: str | None = None
    s3_prefix: str = "skills"
    aws_region: str = "ap-northeast-1"

    cors_origins: str = "http://localhost:3000,http://frontend:3000"

    git_clone_timeout_sec: int = 120
    git_workdir: str = "/app/git_repos"

    # OpenAI (optional) — used by /api/v1/inquire
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = "https://api.openai.com/v1"
    openai_timeout_sec: float = 45.0

    @field_validator("database_url")
    @classmethod
    def _require_sqlalchemy_driver(cls, value: str) -> str:
        # Managed platforms (Railway, Heroku) inject driver-less URLs such as
        # postgres://... which SQLAlchemy cannot resolve to a DBAPI on its own.
        for prefix in ("postgres://", "postgresql://"):
            if value.startswith(prefix):
                return f"postgresql+psycopg2://{value[len(prefix):]}"
        return value

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
