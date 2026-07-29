"""Programmatic pytest runner that exposes results to the Web UI."""

from __future__ import annotations

import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BACKEND_ROOT = Path(__file__).resolve().parents[2]
TESTS_DIR = BACKEND_ROOT / "tests"

_lock = threading.Lock()
_running = False
_latest: dict[str, Any] | None = None


def _class_name_from_nodeid(nodeid: str) -> str | None:
    if "::" not in nodeid:
        return None
    parts = nodeid.split("::")
    if len(parts) >= 3:
        return parts[1]
    return None


def get_latest_result() -> dict[str, Any] | None:
    return _latest


def is_running() -> bool:
    return _running


def run_tests(*, quiet: bool = True) -> dict[str, Any]:
    """Run the backend test suite and return a JSON-serializable report."""
    global _running, _latest

    try:
        import pytest
    except ImportError:
        report = {
            "status": "error",
            "message": "pytest is not installed in this environment",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "duration_ms": 0,
            "summary": {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "error": 1},
            "tests": [],
            "by_class": [],
        }
        _latest = report
        return report

    if not TESTS_DIR.is_dir():
        report = {
            "status": "error",
            "message": f"tests directory not found: {TESTS_DIR}",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "duration_ms": 0,
            "summary": {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "error": 0},
            "tests": [],
            "by_class": [],
        }
        _latest = report
        return report

    with _lock:
        if _running:
            return {
                "status": "running",
                "message": "Tests are already running",
                "started_at": datetime.now(timezone.utc).isoformat(),
                "finished_at": None,
                "duration_ms": 0,
                "summary": {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "error": 0},
                "tests": [],
                "by_class": [],
                **({"previous": _latest} if _latest else {}),
            }
        _running = True

    class _ResultPlugin:
        def __init__(self) -> None:
            self.tests: list[dict[str, Any]] = []
            self.exitstatus = 0

        def pytest_runtest_logreport(self, report) -> None:
            if report.when != "call" and not (report.when == "setup" and report.failed):
                return
            node = report.nodeid
            existing = next((t for t in self.tests if t["nodeid"] == node), None)
            entry = {
                "nodeid": node,
                "outcome": report.outcome,
                "duration_ms": round(report.duration * 1000, 2),
                "keywords": sorted(
                    k
                    for k in getattr(report, "keywords", {}).keys()
                    if not k.startswith("_")
                )[:12],
            }
            if report.longrepr:
                entry["longrepr"] = str(report.longrepr)[:4000]
            if existing:
                if report.when == "call" or report.failed:
                    existing.update(entry)
            else:
                self.tests.append(entry)

        def pytest_sessionfinish(self, session, exitstatus: int) -> None:  # noqa: ARG002
            self.exitstatus = exitstatus

    plugin = _ResultPlugin()
    started = datetime.now(timezone.utc)
    t0 = time.time()
    args = [str(TESTS_DIR), "-q", "--tb=short"]
    if quiet:
        args.extend(["-p", "no:cacheprovider"])

    try:
        exitstatus = pytest.main(args, plugins=[plugin])
    except Exception as exc:  # pragma: no cover
        finished = datetime.now(timezone.utc)
        report = {
            "status": "error",
            "message": str(exc)[:1000],
            "started_at": started.isoformat(),
            "finished_at": finished.isoformat(),
            "duration_ms": round((time.time() - t0) * 1000, 2),
            "summary": {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "error": 1},
            "tests": [],
            "by_class": [],
        }
        with _lock:
            _latest = report
            _running = False
        return report

    passed = sum(1 for t in plugin.tests if t["outcome"] == "passed")
    failed = sum(1 for t in plugin.tests if t["outcome"] == "failed")
    skipped = sum(1 for t in plugin.tests if t["outcome"] == "skipped")
    error = sum(1 for t in plugin.tests if t["outcome"] == "error")
    total = len(plugin.tests)

    by_class: dict[str, dict[str, Any]] = {}
    for t in plugin.tests:
        cls = _class_name_from_nodeid(t["nodeid"]) or "(module)"
        bucket = by_class.setdefault(
            cls,
            {
                "class_name": cls,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "error": 0,
                "tests": [],
            },
        )
        bucket["tests"].append(t)
        key = (
            t["outcome"]
            if t["outcome"] in {"passed", "failed", "skipped", "error"}
            else "error"
        )
        bucket[key] += 1

    if exitstatus == 0:
        status = "passed"
        message = "All tests passed"
    elif failed or error:
        status = "failed"
        message = f"Failed {failed + error} / {total}"
    else:
        status = "passed"
        message = "Completed with skips"

    finished = datetime.now(timezone.utc)
    report = {
        "status": status,
        "exitstatus": int(exitstatus),
        "message": message,
        "started_at": started.isoformat(),
        "finished_at": finished.isoformat(),
        "duration_ms": round((time.time() - t0) * 1000, 2),
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "error": error,
        },
        "tests": plugin.tests,
        "by_class": sorted(by_class.values(), key=lambda x: x["class_name"]),
    }
    with _lock:
        _latest = report
        _running = False
    return report
