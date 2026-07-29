import io
import re
import zipfile
from pathlib import Path

import frontmatter

from app import messages as msg
from app.config import Settings, get_settings
from app.services.claude_compat import assess_from_parsed


class SkillParseError(Exception):
    pass


def _find_skill_md(names: list[str]) -> str | None:
    """Prefer SKILL.md at root, then first nested SKILL.md."""
    normalized = {n.replace("\\", "/"): n for n in names}
    for candidate in ("SKILL.md", "skill.md"):
        if candidate in normalized:
            return normalized[candidate]
    for path, original in normalized.items():
        if path.lower().endswith("/skill.md") or path.lower() == "skill.md":
            return original
    return None


def parse_skill_markdown(content: str) -> dict:
    """Parse SKILL.md with optional YAML frontmatter."""
    has_frontmatter = content.lstrip().startswith("---")
    try:
        post = frontmatter.loads(content)
    except Exception:
        return {
            "name": None,
            "frontmatter_name": None,
            "description": content[:500],
            "version": None,
            "author": None,
            "category": None,
            "tags": [],
            "body": content,
            "has_frontmatter": False,
        }

    meta = dict(post.metadata or {})
    frontmatter_name = meta.get("name")
    if frontmatter_name is not None and not isinstance(frontmatter_name, str):
        frontmatter_name = str(frontmatter_name)

    # Catalog may still use title as a display fallback, but Claude requires `name`.
    name = frontmatter_name or meta.get("title")
    description = meta.get("description") or ""
    if not description and post.content:
        for line in post.content.strip().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                description = line[:500]
                break

    tags = meta.get("tags") or meta.get("keywords") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    # Nested metadata map is the Agent Skills-preferred place for extras.
    nested = meta.get("metadata") if isinstance(meta.get("metadata"), dict) else {}
    version = meta.get("version") or nested.get("version")
    if version is not None and not isinstance(version, str):
        version = str(version)
    author = meta.get("author") or meta.get("owner") or nested.get("author")
    category = meta.get("category") or nested.get("category")

    return {
        "name": name,
        "frontmatter_name": frontmatter_name,
        "description": description if isinstance(description, str) else str(description),
        "version": version,
        "author": author,
        "category": category,
        "tags": list(tags) if isinstance(tags, list) else [],
        "body": post.content or content,
        "has_frontmatter": has_frontmatter and bool(meta),
    }


def parse_skill_zip(data: bytes, settings: Settings | None = None) -> dict:
    """Extract and parse a ChatGPT/Cursor/Claude skill ZIP package."""
    from app.services.zip_security import require_skill_metadata, validate_zip_bytes

    settings = settings or get_settings()
    zf = validate_zip_bytes(data, settings)
    try:
        names = [n for n in zf.namelist() if not n.endswith("/")]
        skill_md_name = _find_skill_md(names)
        if not skill_md_name:
            raise SkillParseError(msg.SKILL_MD_NOT_FOUND_IN_ZIP)

        raw = zf.read(skill_md_name).decode("utf-8", errors="strict")
        parsed = parse_skill_markdown(raw)
        require_skill_metadata(parsed)

        parts = skill_md_name.replace("\\", "/").split("/")
        package_dir = parts[-2] if len(parts) >= 2 else None

        parsed["name"] = parsed.get("frontmatter_name") or parsed.get("name")
        parsed["skill_md_content"] = raw
        parsed["file_list"] = names
        parsed["package_dir"] = package_dir
        parsed["claude_compat"] = assess_from_parsed(
            parsed,
            skill_md_path=skill_md_name,
            folder_name=package_dir,
        )
        return parsed
    except UnicodeDecodeError as exc:
        raise SkillParseError(msg.INVALID_ZIP) from exc
    except zipfile.BadZipFile as exc:
        raise SkillParseError(msg.INVALID_ZIP) from exc
    finally:
        zf.close()


def parse_skill_directory(skill_dir: Path) -> dict:
    """Parse a skill directory containing SKILL.md."""
    from app.services.zip_security import require_skill_metadata

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        skill_md = skill_dir / "skill.md"
    if not skill_md.exists():
        raise SkillParseError(msg.skill_md_missing(skill_dir))

    raw = skill_md.read_text(encoding="utf-8", errors="strict")
    parsed = parse_skill_markdown(raw)
    require_skill_metadata(parsed)
    parsed["name"] = parsed.get("frontmatter_name") or parsed.get("name") or skill_dir.name
    parsed["skill_md_content"] = raw
    parsed["package_dir"] = skill_dir.name
    parsed["claude_compat"] = assess_from_parsed(
        parsed,
        folder_name=skill_dir.name,
    )
    return parsed


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    value = re.sub(r"[-\s]+", "-", value)
    return value[:80] or "skill"
