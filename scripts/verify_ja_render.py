"""Fetch the running app and assert that Japanese text reaches the response."""

import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3100"

# Expected Japanese strings, kept as escapes so this file stays ASCII.
CHECKS = [
    ("/", "\u30ab\u30bf\u30ed\u30b0"),
    ("/", "\u793e\u5185\u306e ChatGPT Skills \u3092\u4e00\u5143\u7ba1\u7406"),
    ("/", "\u5229\u7528\u624b\u9806"),
    ("/upload", "Skill \u3092\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9"),
    ("/upload", "\u30bf\u30b0\uff08\u30ab\u30f3\u30de\u533a\u5207\u308a\uff09"),
    ("/git", "Git \u30ea\u30dd\u30b8\u30c8\u30ea\u9023\u643a"),
    ("/api/v1/skills/999999", "Skill \u304c\u898b\u3064\u304b\u308a\u307e\u305b\u3093"),
]

failures = 0
cache: dict[str, str] = {}

for path, expected in CHECKS:
    if path not in cache:
        try:
            with urllib.request.urlopen(BASE + path) as res:
                cache[path] = res.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            # Error payloads are part of what we verify.
            cache[path] = exc.read().decode("utf-8")
    if expected in cache[path]:
        print(f"OK   {path}: {expected}")
    else:
        print(f"FAIL {path}: {expected} not found")
        failures += 1

print(f"{len(CHECKS) - failures}/{len(CHECKS)} checks passed")
sys.exit(1 if failures else 0)
