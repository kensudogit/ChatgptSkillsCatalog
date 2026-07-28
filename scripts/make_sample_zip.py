"""Create a Claude-compatible sample ZIP (folder name == frontmatter name)."""

import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
skill_dir = ROOT / "samples" / "sample-skill"
out = ROOT / "samples" / "sample-pcb-checklist.zip"

raw = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
match = re.search(r"(?m)^name:\s*[\"']?([^\"'\n]+)[\"']?\s*$", raw)
package_name = (match.group(1).strip() if match else "sample-pcb-checklist")

with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
    for path in skill_dir.rglob("*"):
        if path.is_file():
            arc = f"{package_name}/{path.relative_to(skill_dir).as_posix()}"
            zf.write(path, arcname=arc)

print(f"Wrote {out} (package folder: {package_name})")
