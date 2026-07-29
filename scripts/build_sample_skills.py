"""Generate sample Skill packages (UTF-8) and Claude-compatible ZIPs.

All Japanese content is authored as \\uXXXX escapes so this script stays
ASCII-safe on Windows CP1252 consoles.
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "samples"
ZIPS = SAMPLES / "zips"


def _u(s: str) -> str:
    return s.encode("ascii").decode("unicode_escape")


def _skill(name: str, body_esc: str) -> tuple[str, str, str]:
    return (name, f"{name}/SKILL.md", _u(body_esc))


SAMPLES_SPEC = [
    _skill(
        "sample-pcb-checklist",
        r"""---
name: sample-pcb-checklist
description: \u96fb\u5b50\u90e8\u54c1\u30e1\u30fc\u30ab\u30fc\u5411\u3051\u306e PCB \u8a2d\u8a08\u30ec\u30d3\u30e5\u30fc\u30c1\u30a7\u30c3\u30af\u30ea\u30b9\u30c8\u3002\u30dc\u30fc\u30c9\u914d\u7f6e\u30fb\u30af\u30ea\u30a2\u30e9\u30f3\u30b9\u30fb\u71b1\u8a2d\u8a08\u306e\u78ba\u8a8d\u6642\u306b\u4f7f\u7528\u3059\u308b\u3002
metadata:
  version: "1.0.0"
  author: catalog-demo
  category: \u8a2d\u8a08\u30ec\u30d3\u30e5\u30fc
tags: [pcb, checklist, quality]
---

# PCB \u8a2d\u8a08\u30c1\u30a7\u30c3\u30af\u30ea\u30b9\u30c8

PCB \u8a2d\u8a08\u30ec\u30d3\u30e5\u30fc\u306e\u78ba\u8a8d\u9805\u76ee\u3092\u6307\u5c0e\u3059\u308b Skill \u3067\u3059\u3002

## \u30c1\u30a7\u30c3\u30af\u30ea\u30b9\u30c8

1. \u30e9\u30f3\u30c9 / \u30af\u30ea\u30a2\u30e9\u30f3\u30b9\u304c\u793e\u5185\u8a2d\u8a08\u898f\u5247\u306b\u5408\u81f4\u3057\u3066\u3044\u308b
2. \u30c7\u30ab\u30d7\u30ea\u30f3\u30b0\u30b3\u30f3\u30c7\u30f3\u30b5\u304c\u96fb\u6e90\u30d4\u30f3\u8fd1\u508d\u306b\u3042\u308b
3. \u9ad8\u901f\u4fe1\u53f7\u306e\u30a4\u30f3\u30d4\u30fc\u30c0\u30f3\u30b9\u5236\u5fa1\u30fb\u9577\u3055\u6574\u5408
4. \u30b5\u30fc\u30de\u30eb\u30d3\u30a2 / \u9280\u9762\u7a4d\u304c\u71b1\u8a2d\u8a08\u8981\u4ef6\u3092\u6e80\u305f\u3059
5. \u30b7\u30eb\u30af / \u6975\u6027\u8868\u793a\u304c\u8aad\u307f\u53d6\u308c\u308b

## \u4f7f\u3044\u65b9

\u30ec\u30d3\u30e5\u30fc\u5bfe\u8c61\u306e\u8a2d\u8a08\u60c5\u5831\u3092\u63d0\u793a\u3057\u3001\u4e0a\u8a18\u30c1\u30a7\u30c3\u30af\u30ea\u30b9\u30c8\u306b\u7167\u3089\u3057\u3066\u6307\u6458\u3092\u6574\u7406\u3057\u3066\u304f\u3060\u3055\u3044\u3002
""",
    ),
    _skill(
        "bom-cost-review",
        r"""---
name: bom-cost-review
description: \u96fb\u5b50\u90e8\u54c1\u306e BOM \u30b3\u30b9\u30c8\u30fb\u4ee3\u66ff\u54c1\u30fb\u8abf\u9054\u30ea\u30b9\u30af\u3092\u6574\u7406\u3059\u308b\u3002\u539f\u4fa1\u898b\u7a4d\u3084\u4ee3\u66ff\u54c1\u9078\u5b9a\u6642\u306b\u4f7f\u7528\u3059\u308b\u3002
metadata:
  version: "1.0.0"
  author: catalog-demo
  category: \u8abf\u9054
tags: [bom, cost, procurement]
---

# BOM \u30b3\u30b9\u30c8\u30ec\u30d3\u30e5\u30fc

\u96fb\u5b50\u90e8\u54c1\u306e BOM\uff08\u90e8\u54c1\u8868\uff09\u3092\u8aad\u307f\u3001\u30b3\u30b9\u30c8\u30fb\u4ee3\u66ff\u54c1\u30fb\u8abf\u9054\u30ea\u30b9\u30af\u3092\u6574\u7406\u3059\u308b Skill \u3067\u3059\u3002

## \u78ba\u8a8d\u9805\u76ee

1. \u55b6\u696d\u90e8\u54c1\u3068\u975e\u55b6\u696d\u90e8\u54c1\u3092\u533a\u5206\u3059\u308b
2. \u5358\u4fa1\u30fbMOQ\u30fb\u7d0d\u671f\u304c\u5b9f\u7e3e\u306b\u5bfe\u5fdc\u3057\u3066\u3044\u308b\u304b
3. \u4ee3\u66ff\u54c1\uff08\u30d4\u30f3\u4e92\u63db / \u96fb\u6c17\u4ed5\u69d8\uff09\u306e\u6709\u7121
4. \u55b6\u696d\u7d42\u4e86\u30fb\u9577\u7d0d\u671f\u30fb\u5358\u4e00\u5e8f\u5217\u306e\u30ea\u30b9\u30af
5. \u5e63\u7a2e\u30fb\u6ce8\u6587\u5358\u4f4d\u30fb\u904b\u8cc3\u3092\u542b\u3081\u305f\u7dcf\u30b3\u30b9\u30c8

## \u51fa\u529b\u5f62\u5f0f

- \u9ad8\u30b3\u30b9\u30c8\u90e8\u54c1\u30c8\u30c3\u30d7 5
- \u4ee3\u66ff\u6848\uff08\u7406\u7531\u4ed8\u304d\uff09
- \u8abf\u9054\u30ea\u30b9\u30af\u306e\u512a\u5148\u5ea6
""",
    ),
    _skill(
        "datasheet-summarizer",
        r"""---
name: datasheet-summarizer
description: \u96fb\u5b50\u90e8\u54c1\u306e\u30c7\u30fc\u30bf\u30b7\u30fc\u30c8\u304b\u3089\u4e3b\u8981\u4ed5\u69d8\u30fb\u5b9a\u683c\u30fb\u6ce8\u610f\u70b9\u3092\u8981\u7d04\u3059\u308b\u3002PDF \u3084\u30c6\u30ad\u30b9\u30c8\u306e\u8aad\u307f\u89e3\u304d\u6642\u306b\u4f7f\u7528\u3059\u308b\u3002
metadata:
  version: "1.0.0"
  author: catalog-demo
  category: \u30c9\u30ad\u30e5\u30e1\u30f3\u30c8
tags: [datasheet, specs, components]
---

# \u30c7\u30fc\u30bf\u30b7\u30fc\u30c8\u8981\u7d04

\u96fb\u5b50\u90e8\u54c1\u306e\u30c7\u30fc\u30bf\u30b7\u30fc\u30c8\u304b\u3089\u3001\u8a2d\u8a08\u306b\u5fc5\u8981\u306a\u4ed5\u69d8\u3068\u6ce8\u610f\u70b9\u3092\u62bd\u51fa\u3059\u308b Skill \u3067\u3059\u3002

## \u62bd\u51fa\u9805\u76ee

1. \u578b\u756a\u30fb\u30d1\u30c3\u30b1\u30fc\u30b8\u30fb\u30d4\u30f3\u914d\u7f6e
2. \u7d76\u5bfe\u6700\u5927\u5b9a\u683c\uff08\u96fb\u5727 / \u96fb\u6d41 / \u6e29\u5ea6\uff09
3. \u63a8\u5968\u52d5\u4f5c\u6761\u4ef6\u3068\u96fb\u6c17\u7279\u6027
4. \u30c7\u30e9\u30a4\u30c6\u30a3\u30f3\u30b0\u30fb\u52d5\u4f5c\u6642\u9593\u30fb\u30a4\u30f3\u30bf\u30fc\u30d5\u30a7\u30fc\u30b9
5. \u5b9f\u88c5\u4e0a\u306e\u6ce8\u610f\uff08\u30c7\u30ab\u30d7\u30ea\u30f3\u30b0\u3001\u5e03\u7dda\u3001\u71b1\uff09

## \u51fa\u529b

\u8868\u5f62\u5f0f\u3067\u8981\u7d04\u3057\u3001\u4e0d\u660e\u70b9\u306f\u300c\u8981\u78ba\u8a8d\u300d\u3068\u660e\u8a18\u3059\u308b\u3002
""",
    ),
    _skill(
        "esd-protection-guide",
        r"""---
name: esd-protection-guide
description: \u30dd\u30fc\u30c8\u3084 IC \u306e ESD \u4fdd\u8b77\u8a2d\u8a08\u3092\u6307\u5c0e\u3059\u308b\u3002TVS\u30fb\u30af\u30e9\u30f3\u30d7\u30fb\u30dc\u30fc\u30c9\u30ec\u30d9\u30eb\u5bfe\u7b56\u306e\u78ba\u8a8d\u6642\u306b\u4f7f\u7528\u3059\u308b\u3002
metadata:
  version: "1.0.0"
  author: catalog-demo
  category: \u4fe1\u983c\u6027
tags: [esd, protection, reliability]
---

# ESD \u4fdd\u8b77\u30ac\u30a4\u30c9

\u5165\u51fa\u529b\u30dd\u30fc\u30c8\u3084 IC \u306e ESD \u4fdd\u8b77\u8a2d\u8a08\u3092\u78ba\u8a8d\u3059\u308b Skill \u3067\u3059\u3002

## \u30c1\u30a7\u30c3\u30af\u30ea\u30b9\u30c8

1. \u4fdd\u8b77\u30c7\u30d0\u30a4\u30b9\uff08TVS \u7b49\uff09\u304c\u30b3\u30cd\u30af\u30bf\u76f4\u8fd1\u306b\u3042\u308b
2. \u30af\u30e9\u30f3\u30d7\u96fb\u5727\u304c\u88ab\u4fdd\u8b77\u7aef\u5b50\u306e\u8010\u5727\u4ee5\u4e0b
3. \u653e\u96fb\u30d1\u30b9\u304c\u77ed\u304f\u3001\u30b0\u30e9\u30a6\u30f3\u30c9\u3078\u306e\u623b\u308a\u304c\u660e\u78ba
4. \u30b3\u30e2\u30f3\u30e2\u30fc\u30c9 / \u30c7\u30a3\u30d5\u30a1\u30ec\u30f3\u30b7\u30e3\u30eb\u306e\u533a\u5225
5. IEC 61000-4-2 \u7b49\u306e\u76ee\u6a19\u30ec\u30d9\u30eb\u3068\u6574\u5408

## \u51fa\u529b

\u4e0d\u8db3\u70b9\u3068\u6539\u5584\u6848\u3092\u512a\u5148\u5ea6\u4ed8\u304d\u3067\u5217\u6319\u3059\u308b\u3002
""",
    ),
    _skill(
        "soldering-process-qa",
        r"""---
name: soldering-process-qa
description: \u30ea\u30d5\u30ed\u30fc\u30fb\u6d41\u52d5\u306f\u3093\u3060\u4ed8\u3051\u5de5\u7a0b\u306e\u54c1\u8cea\u30c1\u30a7\u30c3\u30af\u30ea\u30b9\u30c8\u3002SMT \u30d7\u30ed\u30d5\u30a1\u30a4\u30eb\u30fb\u4e0d\u5177\u5408\u30fb\u5de5\u7a0b\u7a93\u306e\u78ba\u8a8d\u6642\u306b\u4f7f\u7528\u3059\u308b\u3002
metadata:
  version: "1.0.0"
  author: catalog-demo
  category: \u88fd\u9020
tags: [smt, soldering, quality]
---

# \u306f\u3093\u3060\u4ed8\u3051\u5de5\u7a0b QA

\u30ea\u30d5\u30ed\u30fc / \u6d41\u52d5\u306f\u3093\u3060\u4ed8\u3051\u306e\u5de5\u7a0b\u54c1\u8cea\u3092\u78ba\u8a8d\u3059\u308b Skill \u3067\u3059\u3002

## \u78ba\u8a8d\u9805\u76ee

1. \u30ea\u30d5\u30ed\u30fc\u30d7\u30ed\u30d5\u30a1\u30a4\u30eb\uff08\u4e0a\u6607 / \u30d4\u30fc\u30af / \u51b7\u5374\uff09\u304c\u90e8\u54c1\u8981\u4ef6\u5185
2. \u30d1\u30b9\u30c8\u5370\u5237\u306e\u539a\u307f\u30fb\u30a2\u30d1\u30fc\u30c1\u30e3\u30fb\u30af\u30ea\u30fc\u30cb\u30f3\u30b0
3. \u6a4b\u306e\u5c0f\u5c4b / \u30dc\u30a4\u30c9 / \u5fc3\u504f\u305b / \u672a\u306f\u3093\u3060
4. \u30d5\u30e9\u30c3\u30af\u30b9\u6b8b\u7559\u3068\u6e05\u6d17\u8981\u5426
5. AOI / X\u7dda / \u5916\u89b3\u691c\u67fb\u306e\u5408\u5426\u57fa\u6e96

## \u51fa\u529b

\u4e0d\u5408\u30e2\u30fc\u30c9\u3054\u3068\u306b\u539f\u56e0\u4eee\u8aac\u3068\u6620\u50cf\u3092\u6574\u7406\u3059\u308b\u3002
""",
    ),
]


def write_packages() -> list[Path]:
    SAMPLES.mkdir(parents=True, exist_ok=True)
    ZIPS.mkdir(parents=True, exist_ok=True)
    zip_paths: list[Path] = []

    for package_name, rel_path, content in SAMPLES_SPEC:
        skill_path = SAMPLES / rel_path
        skill_path.parent.mkdir(parents=True, exist_ok=True)
        skill_path.write_text(content, encoding="utf-8", newline="\n")

        if package_name == "sample-pcb-checklist":
            legacy = SAMPLES / "sample-skill" / "SKILL.md"
            legacy.parent.mkdir(parents=True, exist_ok=True)
            legacy.write_text(content, encoding="utf-8", newline="\n")
            readme = SAMPLES / "sample-skill" / "README.md"
            readme.write_text(
                _u(
                    "# sample-pcb-checklist\\n\\n"
                    "Claude \\u4e92\\u63db\\u306e\\u30b5\\u30f3\\u30d7\\u30eb Skill \\u3067\\u3059\\u3002"
                    "ZIP \\u751f\\u6210:\\n\\n"
                    "```bash\\n"
                    "python scripts/build_sample_skills.py\\n"
                    "```\\n"
                ),
                encoding="utf-8",
                newline="\n",
            )

        zip_path = ZIPS / f"{package_name}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            package_root = SAMPLES / package_name
            for path in package_root.rglob("*"):
                if path.is_file():
                    arc = f"{package_name}/{path.relative_to(package_root).as_posix()}"
                    zf.write(path, arcname=arc)
        zip_paths.append(zip_path)

        if package_name == "sample-pcb-checklist":
            legacy_zip = SAMPLES / "sample-pcb-checklist.zip"
            legacy_zip.write_bytes(zip_path.read_bytes())

    return zip_paths


def main() -> None:
    paths = write_packages()
    for p in paths:
        raw = (SAMPLES / p.stem / "SKILL.md").read_text(encoding="utf-8")
        match = re.search(r"(?m)^name:\s*[\"']?([^\"'\n]+)[\"']?\s*$", raw)
        name = match.group(1).strip() if match else p.stem
        assert name == p.stem, (name, p.stem)
        assert "\\u" not in raw
        print(f"wrote {p.relative_to(ROOT)} ({p.stat().st_size} bytes)")
    print(f"ok: {len(paths)} sample skills")


if __name__ == "__main__":
    main()
