"""Insert Claude compat UI strings into frontend messages.ts."""

import re
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "frontend" / "src" / "lib" / "messages.ts"
text = path.read_text(encoding="utf-8")
if "claudeCompat:" in text:
    print("already present")
    raise SystemExit(0)

# Keep this source ASCII-only; decode escapes when building the insert block.
block_escaped = r'''  claudeCompat: {
    label: "Claude",
    ok: "\u4e92\u63db",
    warn: "\u6ce8\u610f",
    error: "\u975e\u4e92\u63db",
    title: "Claude / Agent Skills \u4e92\u63db\u6027",
    lead: "Agent Skills \u4ed5\u69d8\uff08name / description / \u89aa\u30d5\u30a9\u30eb\u30c0\u540d\u4e00\u81f4\uff09\u306b\u57fa\u3065\u304f\u5224\u5b9a\u3067\u3059\u3002ChatGPT\u30fbCursor \u3067\u3082\u540c\u3058 SKILL.md \u3092\u5229\u7528\u3067\u304d\u307e\u3059\u3002",
    noIssues: "\u6307\u6458\u4e8b\u9805\u306f\u3042\u308a\u307e\u305b\u3093\u3002",
    filterAll: "Claude \u5224\u5b9a\u3059\u3079\u3066",
    filterOk: "\u4e92\u63db\u306e\u307f",
    filterWarn: "\u6ce8\u610f\u3042\u308a",
    filterError: "\u975e\u4e92\u63db\u306e\u307f",
  },
'''
block = block_escaped.encode("ascii").decode("unicode_escape")

updated = re.sub(
    r"(  gitExtras: \{.*?\},)\n(\} as const;)",
    r"\1\n" + block + r"\2",
    text,
    count=1,
    flags=re.S,
)
if updated == text:
    raise SystemExit("replace failed")
path.write_text(updated, encoding="utf-8", newline="\n")
print("patched")
