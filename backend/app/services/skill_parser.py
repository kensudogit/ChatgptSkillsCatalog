import io
import re
import zipfile
from pathlib import Path

import frontmatter

from app import messages as msg


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
    try:
        post = frontmatter.loads(content)
    except Exception:
        # Fallback: treat entire file as body
        return {
            "name": None,
            "description": content[:500],
            "version": None,
            "author": None,
            "category": None,
            "tags": [],
            "body": content,
        }

    meta = dict(post.metadata or {})
    name = meta.get("name") or meta.get("title")
    description = meta.get("description") or ""
    if not description and post.content:
        # First non-empty paragraph as description
        for line in post.content.strip().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                description = line[:500]
                break

    tags = meta.get("tags") or meta.get("keywords") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    return {
        "name": name,
        "description": description if isinstance(description, str) else str(description),
        "version": meta.get("version"),
        "author": meta.get("author") or meta.get("owner"),
        "category": meta.get("category"),
        "tags": list(tags) if isinstance(tags, list) else [],
        "body": post.content or content,
    }


def parse_skill_zip(data: bytes) -> dict:
    """Extract and parse a ChatGPT/Cursor skill ZIP package."""
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            names = [n for n in zf.namelist() if not n.endswith("/")]
            skill_md_name = _find_skill_md(names)
            if not skill_md_name:
                raise SkillParseError(msg.SKILL_MD_NOT_FOUND_IN_ZIP)

            raw = zf.read(skill_md_name).decode("utf-8", errors="replace")
            parsed = parse_skill_markdown(raw)

            # Infer name from folder if missing
            if not parsed.get("name"):
                parts = skill_md_name.replace("\\", "/").split("/")
                if len(parts) >= 2:
                    parsed["name"] = parts[-2]
                else:
                    parsed["name"] = "untitled-skill"

            parsed["skill_md_content"] = raw
            parsed["file_list"] = names
            return parsed
    except zipfile.BadZipFile as e:
        raise SkillParseError(msg.INVALID_ZIP) from e


def parse_skill_directory(skill_dir: Path) -> dict:
    """Parse a skill directory containing SKILL.md."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        skill_md = skill_dir / "skill.md"
    if not skill_md.exists():
        raise SkillParseError(msg.skill_md_missing(skill_dir))

    raw = skill_md.read_text(encoding="utf-8", errors="replace")
    parsed = parse_skill_markdown(raw)
    if not parsed.get("name"):
        parsed["name"] = skill_dir.name
    parsed["skill_md_content"] = raw
    return parsed


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    value = re.sub(r"[-\s]+", "-", value)
    return value[:80] or "skill"
