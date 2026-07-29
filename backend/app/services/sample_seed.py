"""Seed sample Skills when the catalog database is empty."""

from __future__ import annotations

import logging
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import Settings
from app.models.skill import Skill, SkillTag
from app.services.skill_parser import parse_skill_zip
from app.services.storage import StorageService

logger = logging.getLogger(__name__)


def _candidate_zip_dirs(settings: Settings) -> list[Path]:
    """Locate packaged sample ZIPs inside the container / workspace."""
    here = Path(__file__).resolve()
    candidates = [
        Path("/app/samples/zips"),
        here.parents[3] / "samples" / "zips",  # repo root when mounted as /app/app/...
        here.parents[2] / "samples" / "zips",
        Path(settings.upload_dir).parent / "samples" / "zips",
    ]
    return [p for p in candidates if p.is_dir()]


def _apply_tags(skill: Skill, tags: list[str]) -> None:
    skill.tags.clear()
    for tag in tags:
        if tag and tag.strip():
            skill.tags.append(SkillTag(tag=tag.strip()[:100]))


def seed_sample_skills(db: Session, settings: Settings) -> dict | None:
    """Idempotently insert sample skills if the catalog is empty."""
    if db.scalar(select(Skill.id).limit(1)) is not None:
        return None

    zip_dirs = _candidate_zip_dirs(settings)
    zips: list[Path] = []
    for d in zip_dirs:
        zips.extend(sorted(d.glob("*.zip")))
    if not zips:
        logger.info("No sample skill ZIPs found; skip seed")
        return None

    storage = StorageService(settings)
    storage.ensure_dirs()
    created = 0
    seen: set[str] = set()

    for zip_path in zips:
        if zip_path.name in seen:
            continue
        seen.add(zip_path.name)
        try:
            data = zip_path.read_bytes()
            parsed = parse_skill_zip(data)
        except Exception as exc:  # pragma: no cover - corrupt sample
            logger.warning("Skip sample %s: %s", zip_path.name, exc)
            continue

        package_dir = parsed.get("package_dir") or zip_path.stem
        tag_list = [str(t) for t in (parsed.get("tags") or [])]
        storage_path = storage.save_bytes(data, zip_path.name, subdir="zips")
        skill = Skill(
            name=parsed["name"],
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

    if created:
        db.commit()
        logger.info("Seeded %s sample skill(s)", created)
    return {"created": created}
