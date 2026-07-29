"""Tests for StorageService."""

import pytest

from app.config import Settings
from app.services.storage import StorageService


class TestStorageService:
    def test_save_read_delete_local(self, settings: Settings):
        storage = StorageService(settings)
        storage.ensure_dirs()
        path = storage.save_bytes(b"hello-zip", "demo.zip", subdir="zips")
        assert path.endswith("demo.zip") or "demo.zip" in path
        assert storage.read_bytes(path) == b"hello-zip"
        local = storage.open_local_path(path)
        assert local is not None and local.exists()
        storage.delete(path)
        with pytest.raises(FileNotFoundError):
            storage.read_bytes(path)

    def test_delete_none_is_noop(self, settings: Settings):
        StorageService(settings).delete(None)

    def test_s3_save_requires_bucket(self, tmp_path):
        settings = Settings(
            database_url="postgresql+psycopg2://u:p@localhost/db",
            upload_dir=str(tmp_path / "up"),
            git_workdir=str(tmp_path / "git"),
            storage_backend="s3",
            s3_bucket=None,
        )
        storage = StorageService(settings)
        with pytest.raises(RuntimeError, match="S3_BUCKET"):
            storage.save_bytes(b"x", "a.zip")

    def test_open_local_path_rejects_s3(self, settings: Settings):
        storage = StorageService(settings)
        assert storage.open_local_path("s3://bucket/key") is None
