"""Unit tests for SKILL.md / ZIP parsing classes and helpers."""

import io
import zipfile
from pathlib import Path

import pytest

from app.services.skill_parser import (
    SkillParseError,
    parse_skill_directory,
    parse_skill_markdown,
    parse_skill_zip,
    slugify,
)


ROOT = Path(__file__).resolve().parents[1]  # backend/ or /app
REPO_ROOT = Path(__file__).resolve().parents[2]


def _samples_root() -> Path:
    for candidate in (
        ROOT / "samples",
        REPO_ROOT / "samples",
        Path("/app/samples"),
    ):
        if candidate.is_dir():
            return candidate
    return REPO_ROOT / "samples"


class TestSkillParseError:
    def test_is_exception(self):
        with pytest.raises(SkillParseError):
            raise SkillParseError("boom")


class TestSlugify:
    def test_basic(self):
        assert "demo" in slugify("Demo Skill!")


class TestParseSkillMarkdown:
    def test_frontmatter(self):
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

    def test_nested_metadata(self):
        content = """---
name: nested-meta
description: Nested metadata sample
metadata:
  version: "2.0.0"
  author: nest-team
  category: docs
tags: [a, b]
---

# Nested
"""
        parsed = parse_skill_markdown(content)
        assert parsed["version"] == "2.0.0"
        assert parsed["author"] == "nest-team"
        assert parsed["category"] == "docs"
        assert parsed["tags"] == ["a", "b"]

    def test_keywords_alias(self):
        content = """---
name: kw-skill
description: Keywords alias sample
keywords: one, two
---

# KW
"""
        parsed = parse_skill_markdown(content)
        assert parsed["tags"] == ["one", "two"]


class TestParseSkillZip:
    def test_sample_zip_is_claude_compatible(self):
        samples = _samples_root()
        zip_path = samples / "sample-pcb-checklist.zip"
        if not zip_path.exists():
            zip_path = samples / "zips" / "sample-pcb-checklist.zip"
        assert zip_path.exists(), zip_path
        parsed = parse_skill_zip(zip_path.read_bytes())
        assert parsed["package_dir"] == "sample-pcb-checklist"
        assert parsed["claude_compat"]["compatible"] is True

    def test_all_sample_zips_are_claude_compatible(self):
        zips_dir = _samples_root() / "zips"
        paths = sorted(zips_dir.glob("*.zip"))
        assert len(paths) >= 5
        for zip_path in paths:
            parsed = parse_skill_zip(zip_path.read_bytes())
            # long-description-warn may be warn but still compatible
            assert parsed["claude_compat"]["compatible"] is True, zip_path.name
            assert parsed["package_dir"] == zip_path.stem

    def test_roundtrip_folder_match(self):
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

    def test_missing_skill_md_raises(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as zf:
            zf.writestr("readme.txt", "no skill")
        with pytest.raises(SkillParseError):
            parse_skill_zip(buffer.getvalue())

    def test_invalid_zip_raises(self):
        with pytest.raises(SkillParseError) as exc:
            parse_skill_zip(b"not-a-zip")
        assert "ZIP" in str(exc.value)


class TestParseSkillDirectory:
    def test_directory(self, tmp_path: Path):
        skill_dir = tmp_path / "dir-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: dir-skill\ndescription: From directory\n---\n\n# Dir\n",
            encoding="utf-8",
        )
        parsed = parse_skill_directory(skill_dir)
        assert parsed["name"] == "dir-skill"
        assert parsed["package_dir"] == "dir-skill"
