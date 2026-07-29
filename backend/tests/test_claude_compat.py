"""Tests for Claude compatibility dataclasses and assess helpers."""

from app.services.claude_compat import (
    ClaudeCompatReport,
    CompatIssue,
    assess_claude_compatibility,
    assess_from_parsed,
    assess_skill_record,
)


class TestCompatIssue:
    def test_fields(self):
        issue = CompatIssue(code="name_missing", severity="error", message="missing")
        assert issue.code == "name_missing"
        assert issue.severity == "error"


class TestClaudeCompatReport:
    def test_to_dict(self):
        report = ClaudeCompatReport(
            compatible=False,
            status="error",
            summary="???",
            issues=[CompatIssue(code="x", severity="error", message="m")],
        )
        data = report.to_dict()
        assert data["compatible"] is False
        assert data["issues"][0]["code"] == "x"


class TestAssessClaudeCompatibility:
    def test_ok(self):
        report = assess_claude_compatibility(
            frontmatter_name="ok-skill",
            description="A valid description for compatibility checks.",
            folder_name="ok-skill",
        )
        assert report.compatible is True
        assert report.status == "ok"

    def test_folder_mismatch_error(self):
        report = assess_claude_compatibility(
            frontmatter_name="ok-skill",
            description="desc",
            folder_name="other-folder",
        )
        assert report.compatible is False
        assert report.status == "error"

    def test_invalid_name(self):
        report = assess_claude_compatibility(
            frontmatter_name="Invalid_Name",
            description="desc",
            folder_name="Invalid_Name",
        )
        assert report.status == "error"

    def test_long_description_warn(self):
        desc = "?" * 201
        report = assess_claude_compatibility(
            frontmatter_name="long-desc-skill",
            description=desc,
            folder_name="long-desc-skill",
        )
        assert report.compatible is True
        assert report.status == "warn"

    def test_missing_frontmatter(self):
        report = assess_claude_compatibility(
            frontmatter_name=None,
            description="",
            folder_name=None,
            has_frontmatter=False,
            folder_required=False,
        )
        assert report.status == "error"


class TestAssessFromParsedAndRecord:
    def test_from_parsed(self):
        data = assess_from_parsed(
            {
                "frontmatter_name": "parsed-skill",
                "description": "Parsed skill description",
                "skill_md_content": (
                    "---\nname: parsed-skill\n"
                    "description: Parsed skill description\n---\n\n# Body\n"
                ),
            },
            folder_name="parsed-skill",
        )
        assert data["compatible"] is True

    def test_assess_skill_record(self):
        data = assess_skill_record(
            skill_md_content=(
                "---\nname: record-skill\n"
                "description: Record based assessment\n---\n\n# Body\n"
            ),
            package_dir="record-skill",
        )
        assert data["status"] in {"ok", "warn", "error"}
