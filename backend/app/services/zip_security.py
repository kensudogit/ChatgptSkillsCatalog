"""ZIP package security and structural validation for Skill uploads."""

from __future__ import annotations

import io
import zipfile
from pathlib import PurePosixPath

from app import messages as msg
from app.config import Settings
from app.services.skill_parser import SkillParseError

ZIP_LOCAL_FILE = b"PK\x03\x04"
ZIP_EMPTY = b"PK\x05\x06"
ZIP_SPANNED = b"PK\x07\x08"


def looks_like_zip(data: bytes) -> bool:
    """Return True when bytes start with a ZIP local/empty/spanned signature."""
    return data.startswith((ZIP_LOCAL_FILE, ZIP_EMPTY, ZIP_SPANNED))


def _is_symlink(info: zipfile.ZipInfo) -> bool:
    # Unix symlink: file type bits 0o120000 in high external_attr.
    return (info.external_attr >> 16) & 0o170000 == 0o120000


def _is_zip_slip(name: str) -> bool:
    norm = name.replace("\\", "/")
    if norm.startswith("/") or norm.startswith("~"):
        return True
    path = PurePosixPath(norm)
    if path.is_absolute():
        return True
    return ".." in path.parts


def _top_level_roots(names: list[str]) -> set[str]:
    roots: set[str] = set()
    for name in names:
        norm = name.replace("\\", "/").lstrip("./")
        if not norm or norm.endswith("/"):
            continue
        parts = PurePosixPath(norm).parts
        if not parts:
            continue
        roots.add(parts[0])
    return roots


def _skill_md_entries(names: list[str]) -> list[str]:
    found: list[str] = []
    for name in names:
        norm = name.replace("\\", "/")
        if PurePosixPath(norm).name.lower() == "skill.md":
            found.append(name)
    return found


def validate_zip_bytes(data: bytes, settings: Settings | None = None) -> zipfile.ZipFile:
    """Validate ZIP magic, structure, and security constraints.

    Returns an open ZipFile. Caller must close it.
    """
    if not looks_like_zip(data):
        raise SkillParseError(msg.INVALID_ZIP_EXTENSION_ONLY)

    settings = settings or Settings()
    try:
        zf = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as exc:
        raise SkillParseError(msg.INVALID_ZIP) from exc

    try:
        infos = zf.infolist()
        file_infos = [i for i in infos if not i.is_dir()]
        if len(file_infos) > settings.max_zip_files:
            raise SkillParseError(msg.too_many_files(settings.max_zip_files))

        total_uncompressed = 0
        for info in file_infos:
            if _is_symlink(info):
                raise SkillParseError(msg.SYMLINK_NOT_ALLOWED)
            if _is_zip_slip(info.filename):
                raise SkillParseError(msg.ZIP_SLIP_DETECTED)

            total_uncompressed += max(0, int(info.file_size))
            compressed = max(1, int(info.compress_size))
            if info.file_size > 0 and (info.file_size / compressed) > settings.max_compression_ratio:
                raise SkillParseError(msg.COMPRESSION_RATIO_TOO_HIGH)

        limit = settings.max_uncompressed_size_mb * 1024 * 1024
        if total_uncompressed > limit:
            raise SkillParseError(msg.uncompressed_too_large(settings.max_uncompressed_size_mb))

        names = [i.filename for i in file_infos]
        skill_mds = _skill_md_entries(names)
        if not skill_mds:
            raise SkillParseError(msg.SKILL_MD_NOT_FOUND_IN_ZIP)
        if len(skill_mds) > 1:
            raise SkillParseError(msg.MULTIPLE_SKILL_MD)

        roots = _top_level_roots(names)
        if len(roots) != 1:
            raise SkillParseError(msg.SINGLE_ROOT_REQUIRED)

        return zf
    except Exception:
        zf.close()
        raise


def require_skill_metadata(parsed: dict) -> None:
    """Reject packages missing required frontmatter fields."""
    name = (parsed.get("frontmatter_name") or "").strip()
    description = (parsed.get("description") or "").strip()
    has_fm = bool(parsed.get("has_frontmatter"))
    if not has_fm or not name or not description:
        raise SkillParseError(msg.MISSING_REQUIRED_METADATA)
