"""Seed sample Skills into the catalog (idempotent by package name)."""

from __future__ import annotations

import io
import sys
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.database import SessionLocal, init_models  # noqa: E402
from app.models.skill import Skill, SkillTag  # noqa: E402
from app.services.skill_parser import parse_skill_zip  # noqa: E402
from app.services.storage import StorageService  # noqa: E402
from app.config import get_settings  # noqa: E402

ZIPS = ROOT / "samples" / "zips"


def _apply_tags(skill: Skill, tags: list[str]) -> None:
    skill.tags.clear()
    for tag in tags:
        if tag and tag.strip():
            skill.tags.append(SkillTag(tag=tag.strip()[:100]))


def seed_from_zips(db: Session, *, force: bool = False) -> dict:
    settings = get_settings()
    storage = StorageService(settings)
    storage.ensure_dirs()

    if not ZIPS.exists():
        raise FileNotFoundError(f"Sample zips not found: {ZIPS}")

    created = 0
    updated = 0
    skipped = 0

    for zip_path in sorted(ZIPS.glob("*.zip")):
        data = zip_path.read_bytes()
        parsed = parse_skill_zip(data)
        package_dir = parsed.get("package_dir") or zip_path.stem
        name = parsed["name"]

        existing = db.scalar(
            select(Skill).where(
                (Skill.package_dir == package_dir) | (Skill.name == name)
            )
        )
        if existing and not force:
            skipped += 1
            continue

        tag_list = [str(t) for t in (parsed.get("tags") or [])]
        storage_path = storage.save_bytes(data, zip_path.name, subdir="zips")

        if existing and force:
            existing.name = name
            existing.description = parsed.get("description") or ""
            existing.version = parsed.get("version")
            existing.author = parsed.get("author")
            existing.category = parsed.get("category")
            existing.source_type = "upload"
            existing.storage_path = storage_path
            existing.original_filename = zip_path.name
            existing.skill_md_content = parsed.get("skill_md_content")
            existing.package_dir = package_dir
            _apply_tags(existing, tag_list)
            updated += 1
        else:
            skill = Skill(
                name=name,
                description=parsed.get("description") or "",
                version=parsed.get("version"),
                author=parsed.get("author"),
                category=parsed.get("category"),
                source_type="upload",
                storage_path=storage_path,
                original_filename=zip_path.name,
                skill_md_content=parsed.get("skill_md_content"),
                package_dir=package_dir,
            )
            db.add(skill)
            db.flush()
            _apply_tags(skill, tag_list)
            created += 1

    db.commit()
    return {"created": created, "updated": updated, "skipped": skipped}


def seed_if_empty(db: Session | None = None) -> dict | None:
    """Insert sample skills when the catalog has zero rows."""
    own_session = db is None
    if own_session:
        db = SessionLocal()
    try:
        count = db.scalar(select(Skill.id).limit(1))
        if count is not None:
            return None
        if not ZIPS.exists() or not any(ZIPS.glob("*.zip")):
            return None
        return seed_from_zips(db)
    finally:
        if own_session:
            db.close()


def main() -> None:
    force = "--force" in sys.argv
    init_models()
    db = SessionLocal()
    try:
        result = seed_from_zips(db, force=force)
    finally:
        db.close()
    print(result)


if __name__ == "__main__":
    main()
