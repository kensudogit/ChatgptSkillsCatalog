"""Append Claude compatibility message helpers (UTF-8)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "backend" / "app" / "messages.py"
text = path.read_text(encoding="utf-8")
if "COMPAT_OK" in text:
    print("already present")
    raise SystemExit(0)

extra = """
# --- Claude / Agent Skills compatibility ---
COMPAT_OK = "Claude \u4e92\u63db"
COMPAT_WARN = "Claude \u4e92\u63db\uff08\u6ce8\u610f\uff09"
COMPAT_ERROR = "Claude \u975e\u4e92\u63db"


def compat_summary_ok() -> str:
    return COMPAT_OK


def compat_summary_warn(count: int) -> str:
    return f"Claude \u4e92\u63db\uff08\u6ce8\u610f {count} \u4ef6\uff09"


def compat_summary_error(count: int) -> str:
    return f"Claude \u975e\u4e92\u63db\uff08{count} \u4ef6\u306e\u30a8\u30e9\u30fc\uff09"


def compat_missing_frontmatter() -> str:
    return "SKILL.md \u5148\u982d\u306b YAML frontmatter\uff08---\uff09\u304c\u3042\u308a\u307e\u305b\u3093"


def compat_name_missing() -> str:
    return "frontmatter \u306e name \u304c\u5fc5\u9808\u3067\u3059"


def compat_name_too_long(length: int, limit: int) -> str:
    return (
        f"name \u306f {limit} \u6587\u5b57\u4ee5\u5185\u3067\u3042\u308b\u5fc5\u8981\u304c\u3042\u308a\u307e\u3059"
        f"\uff08\u73fe\u5728 {length} \u6587\u5b57\uff09"
    )


def compat_name_invalid() -> str:
    return (
        "name \u306f\u5c0f\u6587\u5b57\u82f1\u6570\u5b57\u3068\u30cf\u30a4\u30d5\u30f3\u306e\u307f"
        "\uff08\u5148\u982d\u30fb\u672b\u5c3e\u306e\u30cf\u30a4\u30d5\u30f3\u3001\u9023\u7d9a\u30cf\u30a4\u30d5\u30f3\u4e0d\u53ef\uff09"
    )


def compat_name_reserved(name: str) -> str:
    return f"name\u300c{name}\u300d\u306f\u4e88\u7d04\u8a9e\u306e\u305f\u3081\u4f7f\u7528\u3067\u304d\u307e\u305b\u3093"


def compat_description_missing() -> str:
    return "frontmatter \u306e description \u304c\u5fc5\u9808\u3067\u3059"


def compat_description_too_long(length: int, limit: int) -> str:
    return (
        f"description \u306f {limit} \u6587\u5b57\u4ee5\u5185\u3067\u3042\u308b\u5fc5\u8981\u304c\u3042\u308a\u307e\u3059"
        f"\uff08\u73fe\u5728 {length} \u6587\u5b57\uff09"
    )


def compat_description_claude_ai(length: int, limit: int) -> str:
    return (
        f"Claude.ai \u3078\u306e\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u306f description {limit} \u6587\u5b57\u4ee5\u5185\u63a8\u5968"
        f"\uff08\u73fe\u5728 {length} \u6587\u5b57\uff09\u3002Claude Code / API \u3067\u306f\u554f\u984c\u3042\u308a\u307e\u305b\u3093"
    )


def compat_folder_mismatch(folder: str, name: str) -> str:
    return (
        f"\u89aa\u30d5\u30a9\u30eb\u30c0\u540d\u300c{folder}\u300d\u304c name\u300c{name}\u300d\u3068\u4e00\u81f4\u3057\u3066\u3044\u307e\u305b\u3093\u3002"
        "Claude \u3067\u306f\u4e00\u81f4\u304c\u5fc5\u9808\u3067\u3059"
    )


def compat_folder_unknown() -> str:
    return (
        "\u30d1\u30c3\u30b1\u30fc\u30b8\u306e\u89aa\u30d5\u30a9\u30eb\u30c0\u540d\u3092\u78ba\u8a8d\u3067\u304d\u307e\u305b\u3093\u3067\u3057\u305f\u3002"
        "ZIP \u3067\u306f name \u3068\u540c\u540d\u30d5\u30a9\u30eb\u30c0\u914d\u4e0b\u306b\u7f6e\u3044\u3066\u304f\u3060\u3055\u3044"
    )
"""

path.write_text(text.rstrip() + "\n" + extra + "\n", encoding="utf-8", newline="\n")
print("appended Claude compat messages")
