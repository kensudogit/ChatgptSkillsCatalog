"""Sync sample ZIPs into a running catalog (create missing, refresh existing)."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
ZIPS = ROOT / "samples" / "zips"
BASE = "http://localhost:8000/api/v1"

sys.path.insert(0, str(BACKEND))
from app.services.skill_parser import parse_skill_zip  # noqa: E402


def _list_skills() -> dict[str, dict]:
    data = json.load(urllib.request.urlopen(f"{BASE}/skills?page_size=100"))
    return {item["name"]: item for item in data["items"]}


def _upload(zip_path: Path) -> dict:
    boundary = "----SkillSampleBoundary7MA4YWxk"
    raw = zip_path.read_bytes()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{zip_path.name}"\r\n'
        f"Content-Type: application/zip\r\n\r\n"
    ).encode("utf-8") + raw + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        f"{BASE}/skills/upload",
        data=body,
        method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    return json.load(urllib.request.urlopen(req))


def _patch(skill_id: int, payload: dict) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE}/skills/{skill_id}",
        data=data,
        method="PATCH",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    return json.load(urllib.request.urlopen(req))


def _payload_from_zip(zip_path: Path) -> dict:
    parsed = parse_skill_zip(zip_path.read_bytes())
    return {
        "name": parsed["name"],
        "description": parsed.get("description") or "",
        "version": parsed.get("version"),
        "author": parsed.get("author"),
        "category": parsed.get("category"),
        "tags": [str(t) for t in (parsed.get("tags") or [])],
        "skill_md_content": parsed.get("skill_md_content"),
    }


def main() -> None:
    if not ZIPS.exists():
        raise SystemExit(f"missing {ZIPS}; run build_sample_skills.py first")

    existing = _list_skills()
    created = updated = 0

    for zip_path in sorted(ZIPS.glob("*.zip")):
        name = zip_path.stem
        if name in existing:
            payload = _payload_from_zip(zip_path)
            out = _patch(existing[name]["id"], payload)
            status = out.get("claude_compat", {}).get("status")
            print(f"updated {out['id']} {out['name']} [{status}] tags={out.get('tags')}")
            updated += 1
        else:
            try:
                out = _upload(zip_path)
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")
                raise SystemExit(f"upload failed {zip_path.name}: {exc.code} {detail}") from exc
            status = out.get("claude_compat", {}).get("status")
            print(f"created {out['id']} {out['name']} [{status}]")
            created += 1

    final = json.load(urllib.request.urlopen(f"{BASE}/skills?page_size=100"))
    print(f"done created={created} updated={updated} catalog_total={final['total']}")


if __name__ == "__main__":
    main()
