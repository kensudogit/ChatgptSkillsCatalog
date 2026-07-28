import shutil
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlparse, urlunparse

from git import Repo
from git.exc import GitCommandError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import messages as msg
from app.config import Settings
from app.models.git_source import GitSource
from app.models.skill import Skill, SkillTag
from app.services.skill_parser import SkillParseError, parse_skill_directory


def _authenticated_url(repository_url: str, token: str | None) -> str:
    if not token:
        return repository_url
    parsed = urlparse(repository_url)
    if parsed.scheme not in ("http", "https"):
        return repository_url
    # Use x-access-token style for GitHub/GitLab PAT
    netloc = f"x-access-token:{quote(token, safe='')}@{parsed.hostname}"
    if parsed.port:
        netloc += f":{parsed.port}"
    return urlunparse((parsed.scheme, netloc, parsed.path, "", "", ""))


def _discover_skill_dirs(root: Path) -> list[Path]:
    dirs: list[Path] = []
    for skill_md in root.rglob("SKILL.md"):
        dirs.append(skill_md.parent)
    for skill_md in root.rglob("skill.md"):
        parent = skill_md.parent
        if parent not in dirs:
            dirs.append(parent)
    return dirs


class GitSyncService:
    def __init__(self, settings: Settings):
        self.settings = settings
        Path(settings.git_workdir).mkdir(parents=True, exist_ok=True)

    def sync(self, db: Session, source: GitSource) -> dict:
        workdir = Path(self.settings.git_workdir) / f"source_{source.id}"
        imported = updated = skipped = 0
        skipped_details: list[dict] = []
        try:
            repo = self._clone_or_pull(source, workdir)
            commit = repo.head.commit.hexsha

            search_root = workdir
            if source.skills_subdir:
                search_root = workdir / source.skills_subdir
                if not search_root.exists():
                    raise FileNotFoundError(
                        msg.subdir_missing(source.skills_subdir)
                    )

            skill_dirs = _discover_skill_dirs(search_root)
            seen_paths: set[str] = set()

            for skill_dir in skill_dirs:
                rel = str(skill_dir.relative_to(workdir)).replace("\\", "/")
                seen_paths.add(rel)
                try:
                    parsed = parse_skill_directory(skill_dir)
                except SkillParseError as exc:
                    skipped += 1
                    if len(skipped_details) < 20:
                        skipped_details.append(
                            {"path": rel, "reason": str(exc)[:200]}
                        )
                    continue

                existing = db.scalar(
                    select(Skill).where(
                        Skill.git_source_id == source.id,
                        Skill.git_path == rel,
                    )
                )
                if existing:
                    existing.name = parsed["name"]
                    existing.description = parsed.get("description") or ""
                    existing.version = parsed.get("version")
                    existing.author = parsed.get("author")
                    existing.category = parsed.get("category")
                    existing.skill_md_content = parsed.get("skill_md_content")
                    existing.package_dir = parsed.get("package_dir") or skill_dir.name
                    existing.git_commit = commit
                    existing.source_type = "git"
                    self._replace_tags(db, existing, parsed.get("tags") or [])
                    updated += 1
                else:
                    skill = Skill(
                        name=parsed["name"],
                        description=parsed.get("description") or "",
                        version=parsed.get("version"),
                        author=parsed.get("author"),
                        category=parsed.get("category"),
                        source_type="git",
                        skill_md_content=parsed.get("skill_md_content"),
                        package_dir=parsed.get("package_dir") or skill_dir.name,
                        git_source_id=source.id,
                        git_path=rel,
                        git_commit=commit,
                    )
                    db.add(skill)
                    db.flush()
                    self._replace_tags(db, skill, parsed.get("tags") or [])
                    imported += 1

            # Remove skills that disappeared from repo
            stale = db.scalars(
                select(Skill).where(
                    Skill.git_source_id == source.id,
                    Skill.git_path.is_not(None),
                )
            ).all()
            for skill in stale:
                if skill.git_path not in seen_paths:
                    db.delete(skill)

            source.last_synced_at = datetime.now(timezone.utc)
            source.last_sync_status = "success"
            source.last_sync_message = msg.sync_summary(
                imported, updated, skipped, commit
            )
            db.commit()
            return {
                "git_source_id": source.id,
                "status": "success",
                "message": source.last_sync_message,
                "imported": imported,
                "updated": updated,
                "skipped": skipped,
                "skipped_details": skipped_details,
            }
        except Exception as exc:
            db.rollback()
            source.last_synced_at = datetime.now(timezone.utc)
            source.last_sync_status = "error"
            source.last_sync_message = str(exc)[:1000]
            db.add(source)
            db.commit()
            return {
                "git_source_id": source.id,
                "status": "error",
                "message": str(exc)[:1000],
                "imported": 0,
                "updated": 0,
                "skipped": 0,
                "skipped_details": [],
            }

    def _clone_or_pull(self, source: GitSource, workdir: Path) -> Repo:
        url = _authenticated_url(source.repository_url, source.access_token)
        timeout = max(30, int(self.settings.git_clone_timeout_sec))
        if workdir.exists() and (workdir / ".git").exists():
            repo = Repo(str(workdir))
            # Update remote URL in case token changed
            repo.remotes.origin.set_url(url)
            try:
                with repo.git.custom_environment(GIT_HTTP_LOW_SPEED_TIME=str(timeout)):
                    repo.git.fetch("--all")
                    repo.git.checkout(source.branch)
                    repo.git.pull("origin", source.branch)
            except GitCommandError:
                # Re-clone on hard failure
                shutil.rmtree(workdir, ignore_errors=True)
                return Repo.clone_from(
                    url,
                    str(workdir),
                    branch=source.branch,
                    depth=1,
                )
            return repo

        if workdir.exists():
            shutil.rmtree(workdir, ignore_errors=True)
        return Repo.clone_from(url, str(workdir), branch=source.branch, depth=1)

    @staticmethod
    def _replace_tags(db: Session, skill: Skill, tags: list) -> None:
        skill.tags.clear()
        db.flush()
        for tag in tags:
            if isinstance(tag, str) and tag.strip():
                skill.tags.append(SkillTag(tag=tag.strip()[:100]))
