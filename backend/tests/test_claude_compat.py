"""Unit tests for Claude / Agent Skills compatibility checks."""

from app.services.claude_compat import assess_claude_compatibility


def test_compatible_skill():
    report = assess_claude_compatibility(
        frontmatter_name="pcb-design-review",
        description="PCB design review checklist for electronics manufacturing.",
        folder_name="pcb-design-review",
    )
    assert report.compatible is True
    assert report.status == "ok"


def test_folder_mismatch_is_error():
    report = assess_claude_compatibility(
        frontmatter_name="pcb-design-review",
        description="PCB design review checklist for electronics manufacturing.",
        folder_name="sample-skill",
    )
    assert report.compatible is False
    assert report.status == "error"
    assert any(i.code == "folder_name_mismatch" for i in report.issues)


def test_invalid_name_is_error():
    report = assess_claude_compatibility(
        frontmatter_name="PCB_Review",
        description="Valid description text",
        folder_name="PCB_Review",
    )
    assert report.compatible is False
    assert any(i.code == "name_invalid" for i in report.issues)


def test_long_description_warns_for_claude_ai():
    report = assess_claude_compatibility(
        frontmatter_name="long-desc-skill",
        description="x" * 250,
        folder_name="long-desc-skill",
    )
    assert report.compatible is True
    assert report.status == "warn"
    assert any(i.code == "description_claude_ai_limit" for i in report.issues)
