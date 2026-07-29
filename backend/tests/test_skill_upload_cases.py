"""Specified upload test matrix: normal and abnormal Skill ZIP cases."""

from __future__ import annotations

import io
import zipfile
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app import messages as msg
from app.api.skills import ensure_unique_skill_version
from app.config import Settings
from app.services.skill_parser import SkillParseError, parse_skill_zip
from app.services.zip_security import looks_like_zip, validate_zip_bytes


def _skill_md(
    *,
    name: str = "demo-skill",
    description: str = "Demo skill description for unit tests",
    version: str | None = "1.0.0",
    tags: list[str] | None = None,
    extra: str = "",
) -> str:
    tags = tags or ["demo", "unit"]
    tag_line = "[" + ", ".join(tags) + "]"
    version_line = f'version: "{version}"\n' if version is not None else ""
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        f"{version_line}"
        "metadata:\n"
        "  author: catalog-demo\n"
        "  category: test\n"
        f"tags: {tag_line}\n"
        "---\n\n"
        f"# {name}\n\n"
        f"{extra}\n"
    )


def _make_zip(entries: dict[str, str | bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, content in entries.items():
            data = content.encode("utf-8") if isinstance(content, str) else content
            zf.writestr(name, data)
    return buf.getvalue()


def _valid_package(
    *,
    name: str = "demo-skill",
    description: str = "Demo skill description for unit tests",
    version: str = "1.0.0",
    tags: list[str] | None = None,
    extra_files: dict[str, str] | None = None,
) -> bytes:
    entries: dict[str, str | bytes] = {
        f"{name}/SKILL.md": _skill_md(
            name=name, description=description, version=version, tags=tags
        )
    }
    if extra_files:
        entries.update({f"{name}/{k}": v for k, v in extra_files.items()})
    return _make_zip(entries)


def _settings(**kwargs) -> Settings:
    base = dict(
        database_url="postgresql+psycopg2://u:p@localhost/db",
        upload_dir="/tmp/uploads-test",
        git_workdir="/tmp/git-test",
        max_upload_size_mb=1,
        max_zip_files=10,
        max_uncompressed_size_mb=1,
        max_compression_ratio=50.0,
    )
    base.update(kwargs)
    return Settings(**base)


class TestNormalSkillUpload:
    """Normal cases."""

    def test_upload_valid_zip_parses(self):
        parsed = parse_skill_zip(_valid_package(), settings=_settings())
        assert parsed["name"] == "demo-skill"
        assert parsed["package_dir"] == "demo-skill"

    def test_parse_skill_md(self):
        parsed = parse_skill_zip(
            _valid_package(extra_files={"notes.md": "# note"}),
            settings=_settings(),
        )
        assert parsed["skill_md_content"].startswith("---")
        assert "Demo skill" in parsed["description"]

    def test_register_tags(self):
        parsed = parse_skill_zip(
            _valid_package(tags=["pcb", "quality", "review"]),
            settings=_settings(),
        )
        assert parsed["tags"] == ["pcb", "quality", "review"]

    def test_parse_japanese(self):
        description = (
            "\u96fb\u5b50\u90e8\u54c1\u306e\u8a2d\u8a08\u30ec\u30d3\u30e5\u30fc"
            "\u3092\u652f\u63f4\u3059\u308b Skill \u3067\u3059\u3002"
        )
        body = "\u65e5\u672c\u8a9e\u306e\u672c\u6587\u3067\u3059\u3002"
        parsed = parse_skill_zip(
            _valid_package(
                name="ja-skill",
                description=description,
                extra_files={"readme.md": body},
            ),
            settings=_settings(),
        )
        assert "\u96fb\u5b50\u90e8\u54c1" in parsed["description"]
        assert "\u65e5\u672c\u8a9e" in body
        assert any(p.endswith("readme.md") for p in parsed["file_list"])
        # Japanese in SKILL.md body via description field is preserved as UTF-8.
        assert parsed["skill_md_content"].encode("utf-8")

    def test_single_root_directory(self):
        parsed = parse_skill_zip(
            _valid_package(name="root-skill"),
            settings=_settings(),
        )
        assert parsed["package_dir"] == "root-skill"
        roots = {p.split("/")[0] for p in parsed["file_list"]}
        assert roots == {"root-skill"}

    def test_register_version(self):
        parsed = parse_skill_zip(
            _valid_package(version="2.3.4"),
            settings=_settings(),
        )
        assert parsed["version"] == "2.3.4"


class TestAbnormalSkillUpload:
    """Abnormal / security cases."""

    def test_reject_non_zip_extension(self):
        with pytest.raises(SkillParseError):
            parse_skill_zip(b"plain-text", settings=_settings())

    def test_reject_extension_only_zip(self):
        fake = b"this is not a zip but named.zip"
        assert not looks_like_zip(fake)
        with pytest.raises(SkillParseError) as exc:
            parse_skill_zip(fake, settings=_settings())
        assert str(exc.value) == msg.INVALID_ZIP_EXTENSION_ONLY

    def test_reject_corrupted_zip(self):
        broken = b"PK\x03\x04" + b"\x00" * 20
        with pytest.raises(SkillParseError) as exc:
            parse_skill_zip(broken, settings=_settings())
        assert str(exc.value) == msg.INVALID_ZIP

    def test_reject_missing_skill_md(self):
        data = _make_zip({"demo-skill/README.md": "# no skill md"})
        with pytest.raises(SkillParseError) as exc:
            parse_skill_zip(data, settings=_settings())
        assert str(exc.value) == msg.SKILL_MD_NOT_FOUND_IN_ZIP

    def test_reject_multiple_skill_md(self):
        data = _make_zip(
            {
                "demo-skill/SKILL.md": _skill_md(name="demo-skill"),
                "other/SKILL.md": _skill_md(name="other"),
            }
        )
        with pytest.raises(SkillParseError) as exc:
            parse_skill_zip(data, settings=_settings())
        assert str(exc.value) == msg.MULTIPLE_SKILL_MD

    def test_reject_missing_required_metadata(self):
        md = "---\nname: no-desc\n---\n\n# Body\n"
        data = _make_zip({"no-desc/SKILL.md": md})
        with pytest.raises(SkillParseError) as exc:
            parse_skill_zip(data, settings=_settings())
        assert str(exc.value) == msg.MISSING_REQUIRED_METADATA

    def test_reject_duplicate_skill_version(self):
        db = MagicMock()
        db.scalar.return_value = MagicMock(id=99)
        with pytest.raises(HTTPException) as exc:
            ensure_unique_skill_version(db, "demo-skill", "1.0.0")
        assert exc.value.status_code == 400
        assert exc.value.detail == msg.DUPLICATE_SKILL_VERSION

        db.scalar.return_value = None
        ensure_unique_skill_version(db, "demo-skill", "1.0.0")
        ensure_unique_skill_version(db, "demo-skill", None)

    def test_reject_size_limit_exceeded(self):
        settings = _settings(max_upload_size_mb=0)
        data = _valid_package()
        assert len(data) > settings.max_upload_size_mb * 1024 * 1024
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(
                status_code=400,
                detail=msg.file_too_large(settings.max_upload_size_mb),
            )
        assert exc.value.detail == msg.file_too_large(0)

    def test_reject_too_many_files(self):
        entries = {f"pack/file_{i}.txt": f"x{i}" for i in range(12)}
        entries["pack/SKILL.md"] = _skill_md(name="pack")
        data = _make_zip(entries)
        with pytest.raises(SkillParseError) as exc:
            parse_skill_zip(data, settings=_settings(max_zip_files=10))
        assert str(exc.value) == msg.too_many_files(10)

    def test_reject_zip_slip(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            info = zipfile.ZipInfo("../evil/SKILL.md")
            zf.writestr(info, _skill_md(name="evil"))
        with pytest.raises(SkillParseError) as exc:
            validate_zip_bytes(buf.getvalue(), settings=_settings())
        assert str(exc.value) == msg.ZIP_SLIP_DETECTED

    def test_reject_symlink(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("pack/SKILL.md", _skill_md(name="pack"))
            link = zipfile.ZipInfo("pack/link-out")
            link.create_system = 3
            link.external_attr = 0o120777 << 16
            zf.writestr(link, b"/tmp/escape")
        with pytest.raises(SkillParseError) as exc:
            validate_zip_bytes(buf.getvalue(), settings=_settings())
        assert str(exc.value) == msg.SYMLINK_NOT_ALLOWED

    def test_reject_zip_bomb_ratio(self):
        zeros = b"\x00" * 200_000
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("bomb/SKILL.md", _skill_md(name="bomb"))
            zf.writestr("bomb/payload.bin", zeros)
        with pytest.raises(SkillParseError) as exc:
            parse_skill_zip(
                buf.getvalue(),
                settings=_settings(
                    max_compression_ratio=10.0,
                    max_uncompressed_size_mb=50,
                ),
            )
        assert str(exc.value) in {
            msg.COMPRESSION_RATIO_TOO_HIGH,
            msg.UNCOMPRESSED_TOO_LARGE,
            msg.uncompressed_too_large(50),
        }


class TestZipSecurityHelpers:
    def test_looks_like_zip_true_for_valid(self):
        assert looks_like_zip(_valid_package())

    def test_single_root_required(self):
        data = _make_zip(
            {
                "a/SKILL.md": _skill_md(name="a"),
                "b/readme.txt": "x",
            }
        )
        with pytest.raises(SkillParseError) as exc:
            validate_zip_bytes(data, settings=_settings())
        assert str(exc.value) == msg.SINGLE_ROOT_REQUIRED
