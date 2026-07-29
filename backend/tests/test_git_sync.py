"""Tests for GitSyncService helpers and class behavior."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

from app.services import git_sync
from app.services.git_sync import GitSyncService, _authenticated_url, _discover_skill_dirs


class TestAuthenticatedUrl:
    def test_without_token(self):
        url = "https://github.com/org/repo.git"
        assert _authenticated_url(url, None) == url

    def test_with_token(self):
        url = _authenticated_url("https://github.com/org/repo.git", "tok en")
        assert "x-access-token:" in url
        assert "@github.com" in url
        assert url.startswith("https://")

    def test_non_http_unchanged(self):
        url = "git@github.com:org/repo.git"
        assert _authenticated_url(url, "token") == url


class TestDiscoverSkillDirs:
    def test_finds_skill_md(self, tmp_path: Path):
        skill = tmp_path / "pack" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("---\nname: pack\ndescription: d\n---\n", encoding="utf-8")
        found = _discover_skill_dirs(tmp_path)
        assert skill.parent in found


class TestGitSyncService:
    def test_init_creates_workdir(self, settings):
        svc = GitSyncService(settings)
        assert Path(settings.git_workdir).exists()
        assert svc.settings is settings

    def test_replace_tags(self, settings):
        skill = SimpleNamespace(tags=[])
        db = MagicMock()
        GitSyncService._replace_tags(db, skill, ["a", " b ", "", 123])
        assert [t.tag for t in skill.tags] == ["a", "b"]

    def test_sync_error_when_subdir_missing(self, settings, fake_git_source):
        svc = GitSyncService(settings)
        fake_git_source.skills_subdir = "missing-dir"
        fake_git_source.id = 99

        repo = MagicMock()
        repo.head.commit.hexsha = "abc123"
        svc._clone_or_pull = MagicMock(return_value=repo)  # type: ignore[method-assign]

        db = MagicMock()
        result = svc.sync(db, fake_git_source)
        assert result["status"] == "error"
        assert result["imported"] == 0
