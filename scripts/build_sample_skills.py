"""Generate 10 sample Skills with diverse SKILL.md / package formats.

Japanese text is authored as \\uXXXX escapes so this script stays ASCII-safe
on Windows CP1252 consoles.
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


# Extra files placed beside SKILL.md: (relative_path, content_esc)
# Spec entry: (package_name, skill_md_esc, extra_files)
SampleSpec = tuple[str, str, list[tuple[str, str]]]


def _spec(name: str, skill_esc: str, extras: list[tuple[str, str]] | None = None) -> SampleSpec:
    return (name, skill_esc, extras or [])


SAMPLES_SPEC: list[SampleSpec] = [
    # 01 -- Canonical Agent Skills: nested metadata + tags array
    _spec(
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
""",
    ),
    # 02 -- Flat top-level version/author/category (catalog-friendly, not nested)
    _spec(
        "bom-cost-review",
        r"""---
name: bom-cost-review
description: \u96fb\u5b50\u90e8\u54c1\u306e BOM \u30b3\u30b9\u30c8\u30fb\u4ee3\u66ff\u54c1\u30fb\u8abf\u9054\u30ea\u30b9\u30af\u3092\u6574\u7406\u3059\u308b\u3002\u539f\u4fa1\u898b\u7a4d\u3084\u4ee3\u66ff\u54c1\u9078\u5b9a\u6642\u306b\u4f7f\u7528\u3059\u308b\u3002
version: 1.2.0
author: sourcing-team
category: \u8abf\u9054
tags:
  - bom
  - cost
  - procurement
---

# BOM \u30b3\u30b9\u30c8\u30ec\u30d3\u30e5\u30fc

\u96fb\u5b50\u90e8\u54c1\u306e BOM\uff08\u90e8\u54c1\u8868\uff09\u3092\u8aad\u307f\u3001\u30b3\u30b9\u30c8\u30fb\u4ee3\u66ff\u54c1\u30fb\u8abf\u9054\u30ea\u30b9\u30af\u3092\u6574\u7406\u3059\u308b Skill \u3067\u3059\u3002

## \u51fa\u529b\u5f62\u5f0f

| \u9805\u76ee | \u5185\u5bb9 |
|------|------|
| \u9ad8\u30b3\u30b9\u30c8 | Top 5 \u90e8\u54c1 |
| \u4ee3\u66ff\u6848 | \u7406\u7531\u4ed8\u304d |
| \u30ea\u30b9\u30af | \u512a\u5148\u5ea6\u4ed8\u304d |
""",
    ),
    # 03 -- Quoted description + keywords alias instead of tags
    _spec(
        "datasheet-summarizer",
        r"""---
name: datasheet-summarizer
description: "\u96fb\u5b50\u90e8\u54c1\u306e\u30c7\u30fc\u30bf\u30b7\u30fc\u30c8\u304b\u3089\u4e3b\u8981\u4ed5\u69d8\u30fb\u5b9a\u683c\u30fb\u6ce8\u610f\u70b9\u3092\u8981\u7d04\u3059\u308b\u3002PDF \u3084\u30c6\u30ad\u30b9\u30c8\u306e\u8aad\u307f\u89e3\u304d\u6642\u306b\u4f7f\u7528\u3059\u308b\u3002"
metadata:
  version: "2.0.0"
  author: doc-team
  category: \u30c9\u30ad\u30e5\u30e1\u30f3\u30c8
keywords: datasheet, specs, components
---

# \u30c7\u30fc\u30bf\u30b7\u30fc\u30c8\u8981\u7d04

## \u62bd\u51fa\u30c6\u30f3\u30d7\u30ec\u30fc\u30c8

```text
\u578b\u756a:
\u30d1\u30c3\u30b1\u30fc\u30b8:
\u7d76\u5bfe\u6700\u5927\u5b9a\u683c:
\u63a8\u5968\u52d5\u4f5c\u6761\u4ef6:
\u5b9f\u88c5\u4e0a\u306e\u6ce8\u610f:
```
""",
    ),
    # 04 -- Package with references/ companion docs
    _spec(
        "esd-protection-guide",
        r"""---
name: esd-protection-guide
description: \u30dd\u30fc\u30c8\u3084 IC \u306e ESD \u4fdd\u8b77\u8a2d\u8a08\u3092\u6307\u5c0e\u3059\u308b\u3002TVS\u30fb\u30af\u30e9\u30f3\u30d7\u30fb\u30dc\u30fc\u30c9\u30ec\u30d9\u30eb\u5bfe\u7b56\u306e\u78ba\u8a8d\u6642\u306b\u4f7f\u7528\u3059\u308b\u3002
metadata:
  version: "1.0.1"
  author: reliability-lab
  category: \u4fe1\u983c\u6027
tags: [esd, protection, reliability]
---

# ESD \u4fdd\u8b77\u30ac\u30a4\u30c9

\u8a73\u7d30\u306a\u57fa\u6e96\u5024\u306f `references/iec-notes.md` \u3092\u53c2\u7167\u3057\u3066\u304f\u3060\u3055\u3044\u3002

## \u30c1\u30a7\u30c3\u30af\u30ea\u30b9\u30c8

1. \u4fdd\u8b77\u30c7\u30d0\u30a4\u30b9\uff08TVS \u7b49\uff09\u304c\u30b3\u30cd\u30af\u30bf\u76f4\u8fd1\u306b\u3042\u308b
2. \u30af\u30e9\u30f3\u30d7\u96fb\u5727\u304c\u88ab\u4fdd\u8b77\u7aef\u5b50\u306e\u8010\u5727\u4ee5\u4e0b
3. \u653e\u96fb\u30d1\u30b9\u304c\u77ed\u304f\u3001\u30b0\u30e9\u30a6\u30f3\u30c9\u3078\u306e\u623b\u308a\u304c\u660e\u78ba
""",
        [
            (
                "references/iec-notes.md",
                r"""# IEC 61000-4-2 \u30e1\u30e2

| Level | Contact | Air |
|-------|---------|-----|
| 2 | 4 kV | 4 kV |
| 4 | 8 kV | 15 kV |

\u76ee\u6a19\u30ec\u30d9\u30eb\u3068\u88ab\u4fdd\u8b77\u7aef\u5b50\u306e\u8010\u5727\u3092\u5fc5\u305a\u5bfe\u6bd4\u3059\u308b\u3002
""",
            )
        ],
    ),
    # 05 -- Package with scripts/ helper
    _spec(
        "soldering-process-qa",
        r"""---
name: soldering-process-qa
description: \u30ea\u30d5\u30ed\u30fc\u30fb\u6d41\u52d5\u306f\u3093\u3060\u4ed8\u3051\u5de5\u7a0b\u306e\u54c1\u8cea\u30c1\u30a7\u30c3\u30af\u30ea\u30b9\u30c8\u3002SMT \u30d7\u30ed\u30d5\u30a1\u30a4\u30eb\u30fb\u4e0d\u5177\u5408\u30fb\u5de5\u7a0b\u7a93\u306e\u78ba\u8a8d\u6642\u306b\u4f7f\u7528\u3059\u308b\u3002
metadata:
  version: "1.0.0"
  author: mfg-qa
  category: \u88fd\u9020
tags: [smt, soldering, quality]
---

# \u306f\u3093\u3060\u4ed8\u3051\u5de5\u7a0b QA

\u30d7\u30ed\u30d5\u30a1\u30a4\u30eb CSV \u306f `scripts/check_profile.py` \u3067\u4e88\u5099\u691c\u67fb\u3067\u304d\u307e\u3059\u3002

## \u78ba\u8a8d\u9805\u76ee

1. \u4e0a\u6607 / \u30d4\u30fc\u30af / \u51b7\u5374\u304c\u90e8\u54c1\u8981\u4ef6\u5185
2. \u30d1\u30b9\u30c8\u539a\u307f\u30fb\u30a2\u30d1\u30fc\u30c1\u30e3\u30fb\u30af\u30ea\u30fc\u30cb\u30f3\u30b0
3. \u6a4b\u306e\u5c0f\u5c4b / \u30dc\u30a4\u30c9 / \u5fc3\u504f\u305b / \u672a\u306f\u3093\u3060
""",
        [
            (
                "scripts/check_profile.py",
                r'''"""Minimal helper: print peak temperature from a CSV column named peak_c."""
import csv
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "profile.csv"
with open(path, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
peaks = [float(r["peak_c"]) for r in rows if r.get("peak_c")]
print(f"samples={len(peaks)} max_peak_c={max(peaks) if peaks else 'n/a'}")
''',
            )
        ],
    ),
    # 06 -- Minimal frontmatter: name + description only
    _spec(
        "minimal-frontmatter",
        r"""---
name: minimal-frontmatter
description: \u6700\u5c0f\u69cb\u6210\u306e Skill \u30b5\u30f3\u30d7\u30eb\u3002name \u3068 description \u306e\u307f\u3092 frontmatter \u306b\u6301\u3064\u3002
---

# \u6700\u5c0f frontmatter

Agent Skills \u3067\u5fc5\u9808\u306a\u306e\u306f `name` \u3068 `description` \u3067\u3059\u3002

version / author / category / tags \u306f\u7701\u7565\u53ef\u80fd\u3067\u3059\uff08\u30ab\u30bf\u30ed\u30b0\u8868\u793a\u306f\u7a7a\u306b\u306a\u308a\u307e\u3059\uff09\u3002

## \u4f7f\u3044\u65b9

\u3053\u306e Skill \u3092\u958b\u3044\u3066\u3001\u6700\u5c0f\u69cb\u6210\u3067\u3082 Claude / ChatGPT / Cursor \u306b\u8aad\u307f\u8fbc\u307e\u308c\u308b\u3053\u3068\u3092\u78ba\u8a8d\u3057\u3066\u304f\u3060\u3055\u3044\u3002
""",
    ),
    # 07 -- Long description (>200 chars) -> Claude.ai warn, still compatible
    _spec(
        "long-description-warn",
        r"""---
name: long-description-warn
description: \u96fb\u5b50\u90e8\u54c1\u306e\u4fe1\u983c\u6027\u8a66\u9a13\uff08\u9ad8\u6e29/\u4f4e\u6e29\u30b5\u30a4\u30af\u30eb\u3001\u6e7f\u5ea6\u3001\u9707\u52d5\u3001\u843d\u4e0b\u3001\u586b\u5de5\u30fb\u91c8\u51fa\u30fb\u5c4a\u66f2\uff09\u306e\u8a08\u753b\u66f8\u3092\u691c\u8a3c\u3057\u3001\u8a66\u9a13\u6761\u4ef6\u30fb\u30b5\u30f3\u30d7\u30eb\u6570\u30fb\u5408\u5426\u57fa\u6e96\u30fb\u5831\u544a\u66f8\u5f0f\u30fb\u8a2d\u5099\u8981\u4ef6\u3092\u6574\u7406\u3059\u308b\u3002\u8a2d\u8a08\u54c1\u8cea\u30fb\u88fd\u9020\u54c1\u8cea\u30fb\u8abf\u9054\u3068\u9023\u643a\u3057\u3001IEC / JEDEC / AEC / \u793e\u5185\u898f\u683c\u306e\u5dee\u7570\u3092\u660e\u793a\u3057\u3001\u8981\u4fee\u6b63\u9805\u76ee\u3068\u30ea\u30b9\u30af\u8a55\u4fa1\u3092\u63d0\u6848\u3059\u308b\u305f\u3081\u306e\u66f8\u5f0f\u7814\u7a76\u7528 Skill\u3002\u8ffd\u52a0\u306e\u78ba\u8a8d\u9805\u76ee\u3068\u3057\u3066\u3001\u8a66\u9a13\u30b7\u30fc\u30b1\u30f3\u30b9\u3001\u74b0\u5883\u6761\u4ef6\u306e\u8a18\u9332\u65b9\u6cd5\u3001\u5931\u6557\u6642\u306e\u518d\u8a66\u9a13\u57fa\u6e96\u3082\u542b\u3081\u3066\u89e3\u8aac\u3059\u308b\u3002
metadata:
  version: "1.0.0"
  author: catalog-demo
  category: \u4fe1\u983c\u6027
tags: [reliability, test, format-study]
---

# \u9577\u3044 description\uff08Claude.ai \u6ce8\u610f\uff09

`description` \u304c 200 \u6587\u5b57\u8d85\uff08Claude.ai \u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u63a8\u5968\u4e0a\u9650\uff09\u306e\u4f8b\u3067\u3059\u3002

Agent Skills \u4ed5\u69d8\u4e0a\u306e\u4e0a\u9650\u306f 1024 \u6587\u5b57\u3067\u3059\u3002\u3053\u306e\u30b5\u30f3\u30d7\u30eb\u306f\u4e92\u63db\uff08\u6ce8\u610f\uff09\u3068\u5224\u5b9a\u3055\u308c\u307e\u3059\u3002

## \u78ba\u8a8d\u30dd\u30a4\u30f3\u30c8

- \u8a66\u9a13\u6761\u4ef6\u3068\u8981\u4ef6\u4ed5\u69d8\u306e\u5bfe\u5fdc
- \u30b5\u30f3\u30d7\u30eb\u6570\u3068\u4fe1\u983c\u6027\u6c34\u6e96
- \u5831\u544a\u66f8\u306e\u7ae0\u7acb\u3066
""",
    ),
    # 08 -- Mixed: owner alias, YAML block scalar description, both metadata + top tags
    _spec(
        "emc-filter-design",
        r"""---
name: emc-filter-design
description: >
  EMI/EMC \u30d5\u30a3\u30eb\u30bf\u8a2d\u8a08\u3092\u652f\u63f4\u3059\u308b\u3002
  \u30b3\u30e2\u30f3\u30e2\u30fc\u30c9\u30c1\u30e7\u30fc\u30af\u30fbX/Y \u30b3\u30f3\u30c7\u30f3\u30b5\u9078\u5b9a\u6642\u306b\u4f7f\u7528\u3059\u308b\u3002
owner: emc-lab
metadata:
  version: "0.9.0"
  author: emc-lab
  category: \u8a2d\u8a08\u30ec\u30d3\u30e5\u30fc
tags:
  - emc
  - filter
  - noise
---

# EMC \u30d5\u30a3\u30eb\u30bf\u8a2d\u8a08

## \u624b\u9806

1. \u5bfe\u8c61\u30dd\u30fc\u30c8\uff08AC / DC / I/O\uff09\u3092\u7279\u5b9a
2. \u5dee\u52d5\u30e2\u30fc\u30c9\u3068\u30b3\u30e2\u30f3\u30e2\u30fc\u30c9\u3092\u5206\u96e2
3. L / Cx / Cy \u306e\u521d\u671f\u5024\u3092\u63d0\u6848
4. \u5b89\u5168\u898f\u683c\uff08\u6d17\u8074\u96fb\u6d41\u7b49\uff09\u3092\u78ba\u8a8d

## \u51fa\u529b

- \u30d6\u30ed\u30c3\u30af\u56f3\uff08\u6587\u5b57\uff09
- \u90e8\u54c1\u5019\u88dc\u30ea\u30b9\u30c8
- \u6e2c\u5b9a\u9805\u76ee
""",
    ),
    # 09 -- Full package: references + scripts + LICENSE-like note file
    _spec(
        "spi-timing-analyzer",
        r"""---
name: spi-timing-analyzer
description: SPI / I2C \u30bf\u30a4\u30df\u30f3\u30b0\u56f3\u3092\u89e3\u91c8\u3057\u3001\u30bb\u30c3\u30c8\u30a2\u30c3\u30d7\u30fb\u30db\u30fc\u30eb\u30c9\u6642\u9593\u306e\u4e0d\u8db3\u3092\u6307\u6458\u3059\u308b\u3002
metadata:
  version: "1.1.0"
  author: digital-design
  category: \u8a2d\u8a08\u30ec\u30d3\u30e5\u30fc
tags: [spi, i2c, timing, digital]
---

# SPI \u30bf\u30a4\u30df\u30f3\u30b0\u89e3\u6790

`references/timing-glossary.md` \u306e\u7528\u8a9e\u3092\u4f7f\u3044\u3001\u5fc5\u8981\u306a\u3089 `scripts/parse_edges.py` \u3067\u30a8\u30c3\u30b8\u4e00\u89a7\u3092\u6574\u7406\u3057\u307e\u3059\u3002

## \u5165\u529b

- \u30af\u30ed\u30c3\u30af\u5468\u6ce2\u6570
- \u30bb\u30c3\u30c8\u30a2\u30c3\u30d7 / \u30db\u30fc\u30eb\u30c9\uff08ns\uff09
- \u30b9\u30ec\u30fc\u30d6\u578b\u756a\u306e\u6700\u5c0f\u8981\u4ef6

## \u51fa\u529b

- \u88dc\u6b63 / \u8b66\u544a / OK \u306e\u4e09\u6bb5\u5224\u5b9a
- \u30de\u30fc\u30b8\u30f3\u8a08\u7b97
""",
        [
            (
                "references/timing-glossary.md",
                r"""# \u7528\u8a9e

- **tsu** setup time
- **th** hold time
- **tco** clock-to-output
""",
            ),
            (
                "scripts/parse_edges.py",
                r'''"""Print rising-edge indices from a simple 0/1 waveform string."""
import sys
wave = sys.argv[1] if len(sys.argv) > 1 else "0011001110"
edges = [i for i in range(1, len(wave)) if wave[i-1] == "0" and wave[i] == "1"]
print(edges)
''',
            ),
            (
                "NOTES.md",
                r"""# NOTES

\u3053\u306e\u30d1\u30c3\u30b1\u30fc\u30b8\u306f\u66f8\u5f0f\u7814\u7a76\u7528\u30b5\u30f3\u30d7\u30eb\u3067\u3059\u3002
SKILL.md \u4ee5\u5916\u306e\u4f34\u8d70\u30d5\u30a1\u30a4\u30eb\u304c\u3042\u3063\u3066\u3082\u3001\u30ed\u30fc\u30c0\u30fc\u306f SKILL.md \u3092\u5165\u53e3\u306b\u3057\u307e\u3059\u3002
""",
            ),
        ],
    ),
    # 10 -- Instruction-heavy body with progressive disclosure sections
    _spec(
        "failure-analysis-coach",
        r"""---
name: failure-analysis-coach
description: \u96fb\u5b50\u90e8\u54c1\u306e\u4e0d\u5177\u5408\u89e3\u6790\uff08FA\uff09\u624b\u9806\u3092\u5c0e\u304f\u3002\u73fe\u8c61\u6574\u7406\u30fb\u539f\u56e0\u4eee\u8aac\u30fb\u5206\u6790\u624b\u6bb5\u306e\u9078\u5b9a\u6642\u306b\u4f7f\u7528\u3059\u308b\u3002
metadata:
  version: "1.0.0"
  author: quality-eng
  category: \u54c1\u8cea
tags: [fa, quality, 8d]
---

# \u4e0d\u5177\u5408\u89e3\u6790\u30b3\u30fc\u30c1

## When to use

- \u5ba2\u5148\u8a34\u3048 / \u5de5\u5834\u5185\u4e0d\u5177\u5408
- \u518d\u767a\u9632\u6b62\u306e 8D / FTA \u652f\u63f4

## Instructions

1. **\u73fe\u8c61**\uff1a\u4f55\u304c\u3001\u3044\u3064\u3001\u3069\u306e\u6761\u4ef6\u3067\u8d77\u304d\u305f\u304b
2. **\u533a\u5206**\uff1a\u8a2d\u8a08 / \u90e8\u54c1 / \u5de5\u7a0b / \u4f7f\u7528\u74b0\u5883
3. **\u4eee\u8aac**\uff1a3 \u6848\u4ee5\u5185\u306b\u7d5e\u308a\u3001\u691c\u8a3c\u624b\u6bb5\u3092\u63d0\u6848
4. **\u8a3c\u62e0**\uff1a\u5fc5\u8981\u306a\u89e3\u6790\uff08X\u7dda / SEM / \u96fb\u6c17\u8a66\u9a13\uff09
5. **\u6620\u50cf**\uff1a\u6620\u6d41\u30fb\u518d\u767a\u9632\u6b62\u3092\u5206\u3051\u3066\u8a18\u8ff0

## Output format

```markdown
## \u73fe\u8c61
## \u4eee\u8aac
## \u6b21\u306e\u52d5\u4f5c
## \u30ea\u30b9\u30af
```

## Examples

**Input:** \u30ea\u30d5\u30ed\u30fc\u5f8c\u306b QFN \u306e\u958b\u653e\u4e0d\u826f\u304c AOI \u3067\u591a\u767a

**Output:** \u30d1\u30b9\u30c8\u5370\u5237\u91cf / \u30d7\u30ed\u30d5\u30a1\u30a4\u30eb / \u30d1\u30c3\u30c9\u8a2d\u8a08\u306e 3 \u4eee\u8aac\u3092\u512a\u5148\u5ea6\u4ed8\u304d\u3067\u63d0\u793a
""",
    ),
]


def write_packages() -> list[Path]:
    SAMPLES.mkdir(parents=True, exist_ok=True)
    ZIPS.mkdir(parents=True, exist_ok=True)
    zip_paths: list[Path] = []

    for package_name, skill_esc, extras in SAMPLES_SPEC:
        package_root = SAMPLES / package_name
        package_root.mkdir(parents=True, exist_ok=True)
        skill_text = _u(skill_esc)
        (package_root / "SKILL.md").write_text(skill_text, encoding="utf-8", newline="\n")

        for rel, content_esc in extras:
            path = package_root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            # scripts stay ASCII; markdown extras may need unicode unescape
            if rel.endswith(".py"):
                path.write_text(content_esc, encoding="utf-8", newline="\n")
            else:
                path.write_text(_u(content_esc), encoding="utf-8", newline="\n")

        if package_name == "sample-pcb-checklist":
            legacy = SAMPLES / "sample-skill"
            legacy.mkdir(parents=True, exist_ok=True)
            (legacy / "SKILL.md").write_text(skill_text, encoding="utf-8", newline="\n")
            (legacy / "README.md").write_text(
                _u(
                    "# sample-pcb-checklist\\n\\n"
                    "\\u66f8\\u5f0f\\u7814\\u7a76\\u7528\\u30b5\\u30f3\\u30d7\\u30eb\\u306e\\u57fa\\u6e96\\u5f62\\u5f0f\\u3067\\u3059\\u3002"
                    "\\u5168\\u4f53\\u306e\\u751f\\u6210:\\n\\n"
                    "```bash\\n"
                    "python scripts/build_sample_skills.py\\n"
                    "```\\n"
                ),
                encoding="utf-8",
                newline="\n",
            )

        zip_path = ZIPS / f"{package_name}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in package_root.rglob("*"):
                if path.is_file():
                    arc = f"{package_name}/{path.relative_to(package_root).as_posix()}"
                    zf.write(path, arcname=arc)
        zip_paths.append(zip_path)

        if package_name == "sample-pcb-checklist":
            (SAMPLES / "sample-pcb-checklist.zip").write_bytes(zip_path.read_bytes())

    return zip_paths


def write_index() -> None:
    """Write samples/README.md describing format variations (UTF-8)."""
    lines = [
        "# Sample Skills\\uff08\\u66f8\\u5f0f\\u30d0\\u30ea\\u30a8\\u30fc\\u30b7\\u30e7\\u30f3\\uff09",
        "",
        "\\u66f8\\u5f0f\\u7814\\u7a76\\u7528\\u306e\\u30b5\\u30f3\\u30d7\\u30eb 10 \\u4ef6\\u3067\\u3059\\u3002ZIP \\u306f `zips/` \\u4ee5\\u4e0b\\u306b\\u751f\\u6210\\u3055\\u308c\\u307e\\u3059\\u3002",
        "",
        "```bash",
        "python scripts/build_sample_skills.py",
        "python scripts/sync_sample_skills.py",
        "```",
        "",
        "| # | package | \\u8981\\u70b9 |",
        "|---|---------|------|",
        "| 01 | `sample-pcb-checklist` | \\u6a19\\u6e96\\uff1anested `metadata:` + `tags: [...]` |",
        "| 02 | `bom-cost-review` | \\u968e\\u5c64\\u578b `version`/`author`/`category` + YAML \\u30ea\\u30b9\\u30c8 tags + \\u8868 |",
        "| 03 | `datasheet-summarizer` | \\u5f15\\u7528\\u7b26 description + `keywords` \\uff08tags \\u4ee3\\u66ff\\uff09 + \\u30b3\\u30fc\\u30c9\\u30d6\\u30ed\\u30c3\\u30af |",
        "| 04 | `esd-protection-guide` | `references/` \\u4f34\\u8d70\\u30c9\\u30ad\\u30e5\\u30e1\\u30f3\\u30c8 |",
        "| 05 | `soldering-process-qa` | `scripts/` \\u4f34\\u8d70\\u30b9\\u30af\\u30ea\\u30d7\\u30c8 |",
        "| 06 | `minimal-frontmatter` | \\u6700\\u5c0f\\uff1a`name` + `description` \\u306e\\u307f |",
        "| 07 | `long-description-warn` | description > 200 \\u6587\\u5b57\\uff08Claude \\u6ce8\\u610f\\uff09 |",
        "| 08 | `emc-filter-design` | YAML `>` \\u6298\\u308a\\u8fd4\\u3057 description + `owner` \\u30a8\\u30a4\\u30ea\\u30a2\\u30b9 |",
        "| 09 | `spi-timing-analyzer` | references + scripts + NOTES.md \\u306e\\u5b8c\\u5168\\u30d1\\u30c3\\u30b1\\u30fc\\u30b8 |",
        "| 10 | `failure-analysis-coach` | When/Instructions/Examples \\u578b\\u306e\\u9577\\u6587 body |",
        "",
        "## Claude \\u4e92\\u63db\\u306e\\u5171\\u901a\\u898f\\u5247",
        "",
        "- `name` \\u306f\\u534a\\u89d2\\u5c0f\\u6587\\u5b57\\u30fb\\u6570\\u5b57\\u30fb\\u30cf\\u30a4\\u30d5\\u30f3\\u306e\\u307f",
        "- ZIP \\u5185\\u306e\\u89aa\\u30d5\\u30a9\\u30eb\\u30c0\\u540d == `name`",
        "- `description` \\u5fc5\\u9808\\uff081024 \\u6587\\u5b57\\u4ee5\\u5185\\u3001Claude.ai \\u306f 200 \\u6587\\u5b57\\u4ee5\\u5185\\u63a8\\u5968\\uff09",
        "",
    ]
    (SAMPLES / "README.md").write_text(_u("\n".join(lines)), encoding="utf-8", newline="\n")


def main() -> None:
    assert len(SAMPLES_SPEC) == 10, len(SAMPLES_SPEC)
    paths = write_packages()
    write_index()
    for p in paths:
        raw = (SAMPLES / p.stem / "SKILL.md").read_text(encoding="utf-8")
        match = re.search(r"(?m)^name:\s*[\"']?([^\"'\n]+)[\"']?\s*$", raw)
        name = match.group(1).strip() if match else p.stem
        assert name == p.stem, (name, p.stem)
        print(f"wrote {p.relative_to(ROOT)} ({p.stat().st_size} bytes)")
    print(f"ok: {len(paths)} sample skills")


if __name__ == "__main__":
    main()
