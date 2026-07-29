"""Tests for Settings configuration class."""

from app.config import Settings, get_settings


class TestSettings:
    def test_default_app_name(self):
        s = Settings(database_url="postgresql+psycopg2://u:p@localhost/db")
        assert "Skills" in s.app_name or s.app_name

    def test_normalize_postgres_scheme(self):
        s = Settings(database_url="postgres://user:pass@host:5432/db")
        assert s.database_url.startswith("postgresql+psycopg2://")

    def test_normalize_postgresql_scheme(self):
        s = Settings(database_url="postgresql://user:pass@host:5432/db")
        assert s.database_url.startswith("postgresql+psycopg2://")

    def test_cors_origin_list(self):
        s = Settings(
            database_url="postgresql+psycopg2://u:p@localhost/db",
            cors_origins="http://a.com, http://b.com",
        )
        assert s.cors_origin_list == ["http://a.com", "http://b.com"]

    def test_get_settings_cached(self):
        get_settings.cache_clear()
        a = get_settings()
        b = get_settings()
        assert a is b
        get_settings.cache_clear()
