"""Expose pytest results to the Web UI."""

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services import test_runner

router = APIRouter(prefix="/tests", tags=["tests"])


class TestCaseResult(BaseModel):
    nodeid: str
    outcome: str
    duration_ms: float = 0
    longrepr: str | None = None
    keywords: list[str] = Field(default_factory=list)


class TestClassResult(BaseModel):
    class_name: str
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    error: int = 0
    tests: list[TestCaseResult] = Field(default_factory=list)


class TestSummary(BaseModel):
    total: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    error: int = 0


class TestRunResult(BaseModel):
    status: str
    message: str
    started_at: str | None = None
    finished_at: str | None = None
    duration_ms: float = 0
    exitstatus: int | None = None
    summary: TestSummary = Field(default_factory=TestSummary)
    tests: list[TestCaseResult] = Field(default_factory=list)
    by_class: list[TestClassResult] = Field(default_factory=list)
    running: bool = False


@router.get("/status", response_model=TestRunResult)
def tests_status():
    latest = test_runner.get_latest_result()
    if test_runner.is_running():
        base = latest or {
            "status": "running",
            "message": "????????",
            "summary": {},
            "tests": [],
            "by_class": [],
        }
        return TestRunResult(**base, running=True)
    if not latest:
        return TestRunResult(
            status="idle",
            message="????????????????????????????????",
            running=False,
        )
    return TestRunResult(**latest, running=False)


@router.post("/run", response_model=TestRunResult)
def tests_run():
    result = test_runner.run_tests()
    running = result.get("status") == "running" or test_runner.is_running()
    return TestRunResult(**{k: v for k, v in result.items() if k != "previous"}, running=running)
