from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class GitSource(Base):
    __tablename__ = "git_sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    repository_url: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    branch: Mapped[str] = mapped_column(String(200), nullable=False, default="main")
    skills_subdir: Mapped[str] = mapped_column(String(300), nullable=False, default="")
    access_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_sync_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_sync_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    skills: Mapped[list["Skill"]] = relationship("Skill", back_populates="git_source")


from app.models.skill import Skill  # noqa: E402  # type: ignore
