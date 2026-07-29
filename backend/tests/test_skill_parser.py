"""Unit tests for SKILL.md / ZIP parsing."""

import io
import zipfile
from pathlib import Path

from app.services.skill_parser import parse_skill_markdown, parse_skill_zip


ROOT = Path(__file__).resolve().parents[2]


def test_parse_frontmatter_name_and_description():
    content = """---
name: demo-skill
description: Demo skill for unit tests
version: 1.0.0
---

# Demo
"""
    parsed = parse_skill_markdown(content)
    assert parsed["frontmatter_name"] == "demo-skill"
    assert parsed["description"].startswith("Demo skill")
    assert parsed["has_frontmatter"] is True


def test_sample_zip_is_claude_compatible():
    zip_path = ROOT / "samples" / "sample-pcb-checklist.zip"
    if not zip_path.exists():
        zip_path = ROOT / "samples" / "zips" / "sample-pcb-checklist.zip"
    parsed = parse_skill_zip(zip_path.read_bytes())
    assert parsed["package_dir"] == "sample-pcb-checklist"
    assert parsed["claude_compat"]["compatible"] is True


def test_all_sample_zips_are_claude_compatible():
    zips_dir = ROOT / "samples" / "zips"
    paths = sorted(zips_dir.glob("*.zip"))
    assert len(paths) >= 5
    for zip_path in paths:
        parsed = parse_skill_zip(zip_path.read_bytes())
        assert parsed["claude_compat"]["compatible"] is True, zip_path.name
        assert parsed["package_dir"] == zip_path.stem


def test_parse_skill_zip_roundtrip_folder_match():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        zf.writestr(
            "ok-skill/SKILL.md",
            """---
name: ok-skill
description: A valid skill used in roundtrip packaging tests.
---

# OK
""",
        )
    parsed = parse_skill_zip(buffer.getvalue())
    assert parsed["package_dir"] == "ok-skill"
    assert parsed["claude_compat"]["compatible"] is True
