"""Tests for inquiry service (catalog Q&A)."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from app.config import Settings
from app.services.inquiry import answer_inquiry, build_fallback_answer, call_openai


def _settings(**kwargs) -> Settings:
    base = dict(
        database_url="postgresql+psycopg2://u:p@localhost/db",
        upload_dir="/tmp/up",
        git_workdir="/tmp/git",
        openai_api_key=None,
        openai_model="gpt-4o-mini",
    )
    base.update(kwargs)
    return Settings(**base)


class TestInquiryFallback:
    def test_howto_fallback(self):
        text = build_fallback_answer("\u4f7f\u3044\u65b9", [])
        assert "ZIP" in text or "\u30ab\u30bf\u30ed\u30b0" in text

    def test_with_skills(self):
        skill = SimpleNamespace(
            name="demo-skill",
            description="Demo description",
            tags=[],
        )
        text = build_fallback_answer("demo", [skill])
        assert "demo-skill" in text

    def test_answer_without_openai(self):
        db = MagicMock()
        db.scalars.return_value.all.return_value = []
        result = answer_inquiry(db, _settings(), "PCB")
        assert result["mode"] == "fallback"
        assert result["answer"]


class TestInquiryOpenAI:
    def test_call_openai_success(self):
        settings = _settings(openai_api_key="sk-test")
        fake_response = MagicMock()
        fake_response.raise_for_status = MagicMock()
        fake_response.json.return_value = {
            "choices": [{"message": {"content": "AI answer"}}]
        }
        fake_client = MagicMock()
        fake_client.__enter__.return_value = fake_client
        fake_client.post.return_value = fake_response

        with patch("app.services.inquiry.httpx.Client", return_value=fake_client):
            answer = call_openai(settings=settings, question="hello", skills=[])
        assert answer == "AI answer"

    def test_answer_uses_openai_when_configured(self):
        db = MagicMock()
        db.scalars.return_value.all.return_value = []
        settings = _settings(openai_api_key="sk-test")
        with patch(
            "app.services.inquiry.call_openai", return_value="from-openai"
        ) as mocked:
            result = answer_inquiry(db, settings, "ESD")
        mocked.assert_called_once()
        assert result["mode"] == "openai"
        assert result["answer"] == "from-openai"
