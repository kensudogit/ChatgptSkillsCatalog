"""API smoke tests for /health with lifespan mocked."""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient


class TestHealthEndpoint:
    def test_health_ok(self):
        with (
            patch("app.main.init_models"),
            patch("app.main.seed_sample_skills"),
            patch("app.main.SessionLocal", return_value=MagicMock()),
            patch("app.main.StorageService") as storage_cls,
        ):
            storage_cls.return_value.ensure_dirs = MagicMock()
            # Re-import app factory to bind patches before client lifespan
            from app.main import app

            with TestClient(app) as client:
                response = client.get("/health")
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "ok"
                assert "app" in data
