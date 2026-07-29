"""Update catalog skill descriptions from Japanese sample SKILL.md files."""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://localhost:8000/api/v1"

CATEGORY_JA = {
    "design-review": "??????",
    "procurement": "??",
    "documentation": "??????",
    "reliability": "???",
    "manufacturing": "??",
}


def main() -> None:
    skills = json.load(urllib.request.urlopen(f"{BASE}/skills?page_size=100"))["items"]
    for skill in skills:
        name = skill["name"]
        md_path = ROOT / "samples" / name / "SKILL.md"
        if not md_path.exists():
            print(f"skip {name}")
            continue
        text = md_path.read_text(encoding="utf-8")
        desc_match = re.search(r"(?m)^description:\s*(.+)\s*$", text)
        cat_match = re.search(r"(?m)^(?:  )?category:\s*[\"']?([^\"'\n]+)[\"']?\s*$", text)
        desc = desc_match.group(1).strip() if desc_match else skill["description"]
        category = (
            cat_match.group(1).strip()
            if cat_match
            else CATEGORY_JA.get(skill.get("category") or "", skill.get("category"))
        )
        payload = {
            "description": desc,
            "category": category,
            "skill_md_content": text,
        }
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            f"{BASE}/skills/{skill['id']}",
            data=data,
            method="PATCH",
            headers={"Content-Type": "application/json; charset=utf-8"},
        )
        out = json.load(urllib.request.urlopen(req))
        print(f"updated {out['id']} {out['name']} [{out.get('category')}]")
        print(f"  {out['description'][:60]}")


if __name__ == "__main__":
    main()
