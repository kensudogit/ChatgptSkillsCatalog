"""Smoke tests for Claude compatibility checker (stdlib only)."""

import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.services.claude_compat import assess_claude_compatibility, assess_from_parsed


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


r = assess_claude_compatibility(
    frontmatter_name="pcb-review",
    description="PCB design review checklist for electronics manufacturing.",
    folder_name="pcb-review",
)
expect(r.compatible and r.status == "ok", f"valid should be ok: {r}")

r = assess_claude_compatibility(
    frontmatter_name="pcb-review",
    description="PCB design review checklist for electronics manufacturing.",
    folder_name="sample-skill",
)
expect(not r.compatible and r.status == "error", f"mismatch should error: {r}")
expect(any(i.code == "folder_name_mismatch" for i in r.issues), "missing mismatch issue")

r = assess_claude_compatibility(
    frontmatter_name="PCB_Review",
    description="ok description here",
    folder_name="PCB_Review",
)
expect(not r.compatible, f"invalid name should fail: {r}")

zip_path = ROOT / "samples" / "sample-pcb-checklist.zip"
with zipfile.ZipFile(zip_path) as zf:
    names = [n for n in zf.namelist() if not n.endswith("/")]
    skill_md = next(n for n in names if n.lower().endswith("skill.md"))
    raw = zf.read(skill_md).decode("utf-8")
folder = skill_md.replace("\\", "/").split("/")[-2]
name_m = re.search(r"(?m)^name:\s*[\"']?([^\"'\n]+)[\"']?\s*$", raw)
desc_m = re.search(r"(?m)^description:\s*[\"']?([^\"'\n]+)[\"']?\s*$", raw)
parsed = {
    "name": name_m.group(1).strip() if name_m else None,
    "frontmatter_name": name_m.group(1).strip() if name_m else None,
    "description": desc_m.group(1).strip() if desc_m else "",
    "skill_md_content": raw,
}
compat = assess_from_parsed(parsed, skill_md_path=skill_md, folder_name=folder)
expect(folder == "sample-pcb-checklist", folder)
expect(compat["compatible"], f"sample zip should be Claude compatible: {compat}")

print("all claude compat smoke tests passed")
