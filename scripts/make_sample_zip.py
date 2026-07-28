import io
import zipfile
from pathlib import Path

# Create a sample ZIP next to this script for manual upload testing
ROOT = Path(__file__).resolve().parents[1]
skill_dir = ROOT / "samples" / "sample-skill"
out = ROOT / "samples" / "sample-pcb-checklist.zip"

with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
    for path in skill_dir.rglob("*"):
        if path.is_file():
            zf.write(path, arcname=f"sample-skill/{path.relative_to(skill_dir).as_posix()}")

print(f"Wrote {out}")
