from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SkillTagOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tag: str


class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    version: str | None = None
    author: str | None = None
    category: str | None = None
    tags: list[str] = Field(default_factory=list)


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    version: str | None = None
    author: str | None = None
    category: str | None = None
    tags: list[str] | None = None


class SkillOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    version: str | None
    author: str | None
    category: str | None
    source_type: str
    original_filename: str | None
    skill_md_content: str | None
    git_source_id: int | None
    git_path: str | None
    git_commit: str | None
    created_at: datetime
    updated_at: datetime
    tags: list[str] = Field(default_factory=list)

    @classmethod
    def from_orm_skill(cls, skill) -> "SkillOut":
        return cls(
            id=skill.id,
            name=skill.name,
            description=skill.description or "",
            version=skill.version,
            author=skill.author,
            category=skill.category,
            source_type=skill.source_type,
            original_filename=skill.original_filename,
            skill_md_content=skill.skill_md_content,
            git_source_id=skill.git_source_id,
            git_path=skill.git_path,
            git_commit=skill.git_commit,
            created_at=skill.created_at,
            updated_at=skill.updated_at,
            tags=[t.tag for t in skill.tags],
        )


class SkillListResponse(BaseModel):
    items: list[SkillOut]
    total: int
    page: int
    page_size: int


class GitSourceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    repository_url: str = Field(..., min_length=1, max_length=500)
    branch: str = "main"
    skills_subdir: str = ""
    access_token: str | None = None


class GitSourceUpdate(BaseModel):
    name: str | None = None
    branch: str | None = None
    skills_subdir: str | None = None
    access_token: str | None = None


class GitSourceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    repository_url: str
    branch: str
    skills_subdir: str
    has_token: bool = False
    last_synced_at: datetime | None
    last_sync_status: str | None
    last_sync_message: str | None
    created_at: datetime
    updated_at: datetime
    skill_count: int = 0

    @classmethod
    def from_orm_source(cls, source, skill_count: int = 0) -> "GitSourceOut":
        return cls(
            id=source.id,
            name=source.name,
            repository_url=source.repository_url,
            branch=source.branch,
            skills_subdir=source.skills_subdir or "",
            has_token=bool(source.access_token),
            last_synced_at=source.last_synced_at,
            last_sync_status=source.last_sync_status,
            last_sync_message=source.last_sync_message,
            created_at=source.created_at,
            updated_at=source.updated_at,
            skill_count=skill_count,
        )


class SyncResult(BaseModel):
    git_source_id: int
    status: str
    message: str
    imported: int = 0
    updated: int = 0
    skipped: int = 0


class HealthResponse(BaseModel):
    status: str
    app: str
