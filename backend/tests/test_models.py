"""Tests for SQLAlchemy model classes."""

from app.database import Base
from app.models.git_source import GitSource
from app.models.skill import Skill, SkillTag


class TestBase:
    def test_base_is_declarative(self):
        assert hasattr(Base, "metadata")
        assert "skills" in Base.metadata.tables
        assert "skill_tags" in Base.metadata.tables
        assert "git_sources" in Base.metadata.tables


class TestSkill:
    def test_tablename(self):
        assert Skill.__tablename__ == "skills"

    def test_instantiate_minimal(self):
        skill = Skill(name="demo-skill", description="desc", source_type="upload")
        assert skill.name == "demo-skill"
        assert skill.description == "desc"
        assert skill.source_type == "upload"
        assert skill.package_dir is None

    def test_has_indexes(self):
        names = {idx.name for idx in Skill.__table__.indexes}
        assert "ix_skills_updated_at" in names
        assert "ix_skills_source_type" in names


class TestSkillTag:
    def test_tablename(self):
        assert SkillTag.__tablename__ == "skill_tags"

    def test_instantiate(self):
        tag = SkillTag(skill_id=1, tag="pcb")
        assert tag.tag == "pcb"
        assert tag.skill_id == 1


class TestGitSource:
    def test_tablename(self):
        assert GitSource.__tablename__ == "git_sources"

    def test_instantiate(self):
        source = GitSource(
            name="repo",
            repository_url="https://example.com/r.git",
            branch="main",
            skills_subdir="",
        )
        assert source.name == "repo"
        assert source.branch == "main"
        assert source.skills_subdir == ""
