from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import messages as msg
from app.config import Settings, get_settings
from app.database import get_db
from app.models.git_source import GitSource
from app.models.skill import Skill
from app.schemas import (
    GitSourceCreate,
    GitSourceOut,
    GitSourceUpdate,
    SyncResult,
)
from app.services.git_sync import GitSyncService

router = APIRouter(prefix="/git-sources", tags=["git-sources"])


@router.get("", response_model=list[GitSourceOut])
def list_git_sources(db: Session = Depends(get_db)):
    sources = db.scalars(select(GitSource).order_by(GitSource.created_at.desc())).all()
    result = []
    for source in sources:
        count = db.scalar(
            select(func.count(Skill.id)).where(Skill.git_source_id == source.id)
        ) or 0
        result.append(GitSourceOut.from_orm_source(source, skill_count=count))
    return result


@router.post("", response_model=GitSourceOut, status_code=status.HTTP_201_CREATED)
def create_git_source(
    payload: GitSourceCreate,
    db: Session = Depends(get_db),
):
    existing = db.scalar(
        select(GitSource).where(GitSource.repository_url == payload.repository_url)
    )
    if existing:
        raise HTTPException(
            status_code=409, detail=msg.REPOSITORY_ALREADY_REGISTERED
        )

    source = GitSource(
        name=payload.name,
        repository_url=payload.repository_url,
        branch=payload.branch or "main",
        skills_subdir=payload.skills_subdir or "",
        access_token=payload.access_token,
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return GitSourceOut.from_orm_source(source, skill_count=0)


@router.get("/{source_id}", response_model=GitSourceOut)
def get_git_source(source_id: int, db: Session = Depends(get_db)):
    source = db.get(GitSource, source_id)
    if not source:
        raise HTTPException(status_code=404, detail=msg.GIT_SOURCE_NOT_FOUND)
    count = db.scalar(
        select(func.count(Skill.id)).where(Skill.git_source_id == source.id)
    ) or 0
    return GitSourceOut.from_orm_source(source, skill_count=count)


@router.patch("/{source_id}", response_model=GitSourceOut)
def update_git_source(
    source_id: int,
    payload: GitSourceUpdate,
    db: Session = Depends(get_db),
):
    source = db.get(GitSource, source_id)
    if not source:
        raise HTTPException(status_code=404, detail=msg.GIT_SOURCE_NOT_FOUND)

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(source, key, value)
    db.commit()
    db.refresh(source)
    count = db.scalar(
        select(func.count(Skill.id)).where(Skill.git_source_id == source.id)
    ) or 0
    return GitSourceOut.from_orm_source(source, skill_count=count)


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_git_source(source_id: int, db: Session = Depends(get_db)):
    source = db.get(GitSource, source_id)
    if not source:
        raise HTTPException(status_code=404, detail=msg.GIT_SOURCE_NOT_FOUND)
    # Skills remain but lose git_source_id via FK SET NULL
    db.delete(source)
    db.commit()
    return None


@router.post("/{source_id}/sync", response_model=SyncResult)
def sync_git_source(
    source_id: int,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    source = db.get(GitSource, source_id)
    if not source:
        raise HTTPException(status_code=404, detail=msg.GIT_SOURCE_NOT_FOUND)

    result = GitSyncService(settings).sync(db, source)
    if result["status"] == "error":
        # Still return 200 with error payload so UI can show message;
        # client can treat status field.
        pass
    return SyncResult(**result)
