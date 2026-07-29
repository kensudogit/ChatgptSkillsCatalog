"""Tests for Pydantic schema classes."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.schemas import (
    ClaudeCompatOut,
    CompatIssueOut,
    GitSourceCreate,
    GitSourceOut,
    GitSourceUpdate,
    HealthResponse,
    SkillCreate,
    SkillListResponse,
    SkillOut,
    SkillSummary,
    SkillUpdate,
    SyncResult,
    SyncSkipItem,
)


class TestSkillCreate:
    def test_valid(self):
        obj = SkillCreate(name="demo", description="d", tags=["a"])
        assert obj.name == "demo"
        assert obj.tags == ["a"]

    def test_name_required(self):
        with pytest.raises(ValidationError):
            SkillCreate(name="")


class TestSkillUpdate:
    def test_partial(self):
        obj = SkillUpdate(description="updated")
        assert obj.description == "updated"
        assert obj.name is None

    def test_skill_md_content_optional(self):
        obj = SkillUpdate(skill_md_content="# body")
        assert obj.skill_md_content == "# body"


class TestCompatSchemas:
    def test_issue_and_report(self):
        issue = CompatIssueOut(code="x", severity="warn", message="m")
        report = ClaudeCompatOut(
            compatible=True, status="warn", summary="??", issues=[issue]
        )
        assert report.compatible is True
        assert report.issues[0].code == "x"


class TestSkillSummaryFromOrm:
    def test_from_orm_skill(self, fake_skill):
        summary = SkillSummary.from_orm_skill(fake_skill)
        assert summary.id == 1
        assert summary.name == "demo-skill"
        assert summary.tags == ["demo", "unit"]
        assert summary.claude_compat.status in {"ok", "warn", "error"}
        assert summary.downloadable is True

    def test_skill_out_includes_body(self, fake_skill):
        out = SkillOut.from_orm_skill(fake_skill)
        assert out.skill_md_content and out.skill_md_content.startswith("---")


class TestSkillListResponse:
    def test_wrap(self, fake_skill):
        item = SkillSummary.from_orm_skill(fake_skill)
        resp = SkillListResponse(items=[item], total=1, page=1, page_size=20)
        assert resp.total == 1
        assert len(resp.items) == 1


class TestGitSourceSchemas:
    def test_create(self):
        obj = GitSourceCreate(
            name="n",
            repository_url="https://example.com/r.git",
            branch="develop",
        )
        assert obj.branch == "develop"

    def test_update(self):
        obj = GitSourceUpdate(branch="main")
        assert obj.branch == "main"

    def test_from_orm_source(self, fake_git_source):
        out = GitSourceOut.from_orm_source(fake_git_source, skill_count=3)
        assert out.has_token is True
        assert out.skill_count == 3
        assert out.repository_url.endswith(".git")


class TestSyncAndHealth:
    def test_sync_result(self):
        result = SyncResult(
            git_source_id=1,
            status="success",
            message="ok",
            imported=1,
            skipped_details=[SyncSkipItem(path="a/SKILL.md", reason="bad")],
        )
        assert result.imported == 1
        assert result.skipped_details[0].path == "a/SKILL.md"

    def test_health(self):
        h = HealthResponse(status="ok", app="Catalog")
        assert h.status == "ok"
