"""Tests for messages helpers used by APIs."""

from app import messages as msg


class TestMessages:
    def test_core_constants(self):
        assert msg.SKILL_NOT_FOUND
        assert msg.ZIP_REQUIRED
        assert msg.DOWNLOAD_NOT_AVAILABLE

    def test_file_too_large(self):
        text = msg.file_too_large(50)
        assert "50" in text

    def test_compat_summaries(self):
        assert msg.compat_summary_ok()
        assert "1" in msg.compat_summary_warn(1)
        assert "2" in msg.compat_summary_error(2)

    def test_sync_summary(self):
        text = msg.sync_summary(1, 2, 3, "abc")
        assert "1" in text and "2" in text
