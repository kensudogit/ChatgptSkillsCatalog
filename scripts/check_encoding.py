"""Verify that every tracked source file is valid UTF-8 and free of mojibake."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET_SUFFIXES = {".ts", ".tsx", ".py", ".css", ".md", ".json", ".yml", ".sh"}
SKIP_DIRS = {"node_modules", ".next", ".git", "__pycache__", "uploads", "gitwork"}

failures = 0
checked = 0

for path in sorted(ROOT.rglob("*")):
    if not path.is_file() or path.suffix not in TARGET_SUFFIXES:
        continue
    if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
        continue
    raw = path.read_bytes()
    rel = path.relative_to(ROOT)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"NOT UTF-8  {rel}: {exc}")
        failures += 1
        continue
    checked += 1
    if "\ufffd" in text:
        print(f"REPLACEMENT CHAR  {rel}")
        failures += 1

print(f"checked {checked} files, {failures} problem(s)")
sys.exit(1 if failures else 0)
