from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app import messages as msg
from app.config import Settings, get_settings
from app.database import get_db
from app.models.skill import Skill, SkillTag
from app.schemas import SkillListResponse, SkillOut, SkillUpdate
from app.services.skill_parser import SkillParseError, parse_skill_zip
from app.services.storage import StorageService

router = APIRouter(prefix="/skills", tags=["skills"])


def _apply_tags(skill: Skill, tags: list[str]) -> None:
    skill.tags.clear()
    for tag in tags:
        if tag and tag.strip():
            skill.tags.append(SkillTag(tag=tag.strip()[:100]))


@router.get("", response_model=SkillListResponse)
def list_skills(
    q: str | None = Query(None, description=msg.QUERY_SEARCH),
    category: str | None = None,
    source_type: str | None = None,
    tag: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    stmt = select(Skill).options(selectinload(Skill.tags))
    count_stmt = select(func.count(Skill.id))

    filters = []
    if q:
        pattern = f"%{q}%"
        tag_subq = select(SkillTag.skill_id).where(SkillTag.tag.ilike(pattern))
        filters.append(
            or_(
                Skill.name.ilike(pattern),
                Skill.description.ilike(pattern),
                Skill.author.ilike(pattern),
                Skill.id.in_(tag_subq),
            )
        )
    if category:
        filters.append(Skill.category == category)
    if source_type:
        filters.append(Skill.source_type == source_type)
    if tag:
        tag_ids = select(SkillTag.skill_id).where(SkillTag.tag.ilike(tag))
        filters.append(Skill.id.in_(tag_ids))

    for f in filters:
        stmt = stmt.where(f)
        count_stmt = count_stmt.where(f)

    total = db.scalar(count_stmt) or 0
    skills = db.scalars(
        stmt.order_by(Skill.updated_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    return SkillListResponse(
        items=[SkillOut.from_orm_skill(s) for s in skills],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    rows = db.scalars(
        select(Skill.category)
        .where(Skill.category.is_not(None), Skill.category != "")
        .distinct()
        .order_by(Skill.category)
    ).all()
    return {"categories": list(rows)}


@router.get("/tags")
def list_tags(db: Session = Depends(get_db)):
    rows = db.scalars(select(SkillTag.tag).distinct().order_by(SkillTag.tag)).all()
    return {"tags": list(rows)}


@router.get("/{skill_id}", response_model=SkillOut)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.scalar(
        select(Skill).options(selectinload(Skill.tags)).where(Skill.id == skill_id)
    )
    if not skill:
        raise HTTPException(status_code=404, detail=msg.SKILL_NOT_FOUND)
    return SkillOut.from_orm_skill(skill)


@router.post("/upload", response_model=SkillOut, status_code=status.HTTP_201_CREATED)
async def upload_skill(
    file: UploadFile = File(...),
    name: str | None = Form(None),
    description: str | None = Form(None),
    category: str | None = Form(None),
    author: str | None = Form(None),
    version: str | None = Form(None),
    tags: str | None = Form(None, description=msg.QUERY_TAGS),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail=msg.ZIP_REQUIRED)

    data = await file.read()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(data) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=msg.file_too_large(settings.max_upload_size_mb),
        )

    try:
        parsed = parse_skill_zip(data)
    except SkillParseError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    tag_list: list[str] = []
    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    elif parsed.get("tags"):
        tag_list = [str(t) for t in parsed["tags"]]

    storage = StorageService(settings)
    storage_path = storage.save_bytes(data, file.filename, subdir="zips")

    skill = Skill(
        name=name or parsed["name"],
        description=description if description is not None else (parsed.get("description") or ""),
        version=version or parsed.get("version"),
        author=author or parsed.get("author"),
        category=category or parsed.get("category"),
        source_type="upload",
        storage_path=storage_path,
        original_filename=file.filename,
        skill_md_content=parsed.get("skill_md_content"),
    )
    db.add(skill)
    db.flush()
    _apply_tags(skill, tag_list)
    db.commit()
    db.refresh(skill)
    skill = db.scalar(
        select(Skill).options(selectinload(Skill.tags)).where(Skill.id == skill.id)
    )
    return SkillOut.from_orm_skill(skill)


@router.patch("/{skill_id}", response_model=SkillOut)
def update_skill(
    skill_id: int,
    payload: SkillUpdate,
    db: Session = Depends(get_db),
):
    skill = db.scalar(
        select(Skill).options(selectinload(Skill.tags)).where(Skill.id == skill_id)
    )
    if not skill:
        raise HTTPException(status_code=404, detail=msg.SKILL_NOT_FOUND)

    data = payload.model_dump(exclude_unset=True)
    tags = data.pop("tags", None)
    for key, value in data.items():
        setattr(skill, key, value)
    if tags is not None:
        _apply_tags(skill, tags)
    db.commit()
    db.refresh(skill)
    skill = db.scalar(
        select(Skill).options(selectinload(Skill.tags)).where(Skill.id == skill_id)
    )
    return SkillOut.from_orm_skill(skill)


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    skill = db.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail=msg.SKILL_NOT_FOUND)

    if skill.storage_path:
        StorageService(settings).delete(skill.storage_path)
    db.delete(skill)
    db.commit()
    return None
