"""Tests for the in-app pytest runner helpers."""

from app.services.test_runner import _class_name_from_nodeid, get_latest_result, is_running


class TestTestRunner:
    def test_class_name_from_nodeid(self):
        assert (
            _class_name_from_nodeid("tests/test_foo.py::TestFoo::test_bar")
            == "TestFoo"
        )
        assert _class_name_from_nodeid("tests/test_foo.py::test_bar") is None

    def test_idle_state_helpers(self):
        # Does not assert exact latest content (may be set by prior API run).
        assert isinstance(is_running(), bool)
        latest = get_latest_result()
        assert latest is None or isinstance(latest, dict)
