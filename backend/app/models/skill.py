from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Skill(Base):
    __tablename__ = "skills"
    __table_args__ = (
        Index("ix_skills_updated_at", "updated_at"),
        Index("ix_skills_source_type", "source_type"),
        Index("ix_skills_git_source_path", "git_source_id", "git_path"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    author: Mapped[str | None] = mapped_column(String(200), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)

    source_type: Mapped[str] = mapped_column(String(20), nullable=False, default="upload")
    # upload | git
    storage_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    original_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    skill_md_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Parent folder name inside the ZIP / git package (should match frontmatter name for Claude)
    package_dir: Mapped[str | None] = mapped_column(String(200), nullable=True)

    git_source_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("git_sources.id", ondelete="SET NULL"), nullable=True
    )
    git_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    git_commit: Mapped[str | None] = mapped_column(String(64), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        index=True,
    )

    tags: Mapped[list["SkillTag"]] = relationship(
        "SkillTag", back_populates="skill", cascade="all, delete-orphan"
    )
    git_source: Mapped["GitSource | None"] = relationship(
        "GitSource", back_populates="skills"
    )


class SkillTag(Base):
    __tablename__ = "skill_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tag: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    skill: Mapped["Skill"] = relationship("Skill", back_populates="tags")


# Avoid circular import issues at type-check time
from app.models.git_source import GitSource  # noqa: E402
