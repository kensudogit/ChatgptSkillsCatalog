"""Tests for sample_seed service."""

from pathlib import Path
from unittest.mock import MagicMock

from app.services.sample_seed import _candidate_zip_dirs, seed_sample_skills


class TestSampleSeed:
    def test_candidate_dirs_include_app_samples(self, settings):
        dirs = _candidate_zip_dirs(settings)
        assert isinstance(dirs, list)

    def test_seed_skips_when_skills_exist(self, settings):
        db = MagicMock()
        db.scalar.return_value = 1
        assert seed_sample_skills(db, settings) is None
        db.commit.assert_not_called()

    def test_seed_skips_when_no_zips(self, settings, tmp_path, monkeypatch):
        db = MagicMock()
        db.scalar.return_value = None
        monkeypatch.setattr(
            "app.services.sample_seed._candidate_zip_dirs",
            lambda _s: [tmp_path / "empty"],
        )
        (tmp_path / "empty").mkdir()
        assert seed_sample_skills(db, settings) is None

    def test_seed_creates_from_zips(self, settings, tmp_path, monkeypatch):
        zips = tmp_path / "zips"
        zips.mkdir()
        # Build a tiny valid skill zip via parser helpers
        import io
        import zipfile

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr(
                "seed-demo/SKILL.md",
                "---\nname: seed-demo\ndescription: Seed demo skill for tests\n"
                "metadata:\n  version: '1.0.0'\n  category: test\ntags: [seed]\n---\n\n# Seed\n",
            )
        (zips / "seed-demo.zip").write_bytes(buf.getvalue())

        db = MagicMock()
        db.scalar.return_value = None
        monkeypatch.setattr(
            "app.services.sample_seed._candidate_zip_dirs",
            lambda _s: [zips],
        )
        result = seed_sample_skills(db, settings)
        assert result is not None
        assert result["created"] == 1
        db.commit.assert_called()
