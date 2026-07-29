"""Shared fixtures for backend unit tests."""

from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from app.config import Settings


@pytest.fixture
def settings(tmp_path) -> Settings:
    return Settings(
        app_name="Test Catalog",
        database_url="postgresql+psycopg2://skills:skills@localhost:5432/skills_catalog",
        upload_dir=str(tmp_path / "uploads"),
        git_workdir=str(tmp_path / "git"),
        storage_backend="local",
        cors_origins="http://localhost:3000",
        debug=True,
    )


@pytest.fixture
def fake_skill():
    now = datetime.now(timezone.utc)
    return SimpleNamespace(
        id=1,
        name="demo-skill",
        description="???",
        version="1.0.0",
        author="tester",
        category="test",
        source_type="upload",
        storage_path=None,
        original_filename="demo.zip",
        skill_md_content=(
            "---\n"
            "name: demo-skill\n"
            "description: Demo skill for unit tests\n"
            "---\n\n"
            "# Demo\n"
        ),
        package_dir="demo-skill",
        git_source_id=None,
        git_path=None,
        git_commit=None,
        created_at=now,
        updated_at=now,
        tags=[SimpleNamespace(tag="demo"), SimpleNamespace(tag="unit")],
    )


@pytest.fixture
def fake_git_source():
    now = datetime.now(timezone.utc)
    return SimpleNamespace(
        id=10,
        name="demo-repo",
        repository_url="https://github.com/example/skills.git",
        branch="main",
        skills_subdir="skills",
        access_token="secret-token",
        last_synced_at=None,
        last_sync_status=None,
        last_sync_message=None,
        created_at=now,
        updated_at=now,
    )
