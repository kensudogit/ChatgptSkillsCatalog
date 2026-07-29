# -*- coding: utf-8 -*-
"""Generate inquiry.py with Japanese strings via unicode escapes."""

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "backend" / "app" / "services" / "inquiry.py"

SRC = r'''
"""Answer catalog inquiries using retrieved Skills + OpenAI (optional)."""

from __future__ import annotations

import logging
from typing import Any

import httpx
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.config import Settings
from app.models.skill import Skill, SkillTag

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "\u3042\u306a\u305f\u306f\u793e\u5185\u5411\u3051 ChatGPT Skills Catalog \u306e\u6848\u5185\u30a2\u30b7\u30b9\u30bf\u30f3\u30c8\u3067\u3059\u3002\n"
    "\u30e6\u30fc\u30b6\u30fc\u306e\u554f\u3044\u5408\u308f\u305b\u306b\u3001\u767b\u9332\u6e08\u307f Skill \u3068\u30ab\u30bf\u30ed\u30b0\u306e\u4f7f\u3044\u65b9\u306b\u57fa\u3065\u3044\u3066\u65e5\u672c\u8a9e\u3067\u7b54\u3048\u3066\u304f\u3060\u3055\u3044\u3002\n\n"
    "\u56de\u7b54\u30eb\u30fc\u30eb:\n"
    "- \u6839\u62e0\u3068\u306a\u308b Skill \u304c\u3042\u308b\u5834\u5408\u306f\u3001\u305d\u306e\u540d\u524d\u3092\u660e\u793a\u3059\u308b\n"
    "- \u30ab\u30bf\u30ed\u30b0\u306b\u7121\u3044\u5185\u5bb9\u306f\u63a8\u6e2c\u3057\u3059\u304e\u305a\u3001\u300c\u767b\u9332\u304c\u898b\u3064\u304b\u308a\u307e\u305b\u3093\u300d\u3068\u4f1d\u3048\u308b\n"
    "- \u624b\u9806\u3092\u805e\u304b\u308c\u305f\u3089\u3001\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9 / Git \u9023\u643a / \u691c\u7d22 / \u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u3092\u7c21\u6f54\u306b\u6848\u5185\u3059\u308b\n"
    "- \u6a5f\u5bc6\u60c5\u5831\u3084\u8a8d\u8a3c\u60c5\u5831\u306e\u53d6\u308a\u6271\u3044\u306b\u306f\u6ce8\u610f\u3092\u4fc3\u3059\n"
    "- \u7c21\u6f54\u3067\u5b9f\u52d9\u7684\u306a\u30c8\u30fc\u30f3\u306b\u3059\u308b\n"
)

CATALOG_HOWTO = (
    "# \u30ab\u30bf\u30ed\u30b0\u306e\u4f7f\u3044\u65b9\uff08\u8981\u7d04\uff09\n"
    "- \u30ab\u30bf\u30ed\u30b0: Skill \u306e\u691c\u7d22\u30fb\u7d5e\u308a\u8fbc\u307f\u30fbClaude \u4e92\u63db\u8868\u793a\n"
    "- \u30a2\u30c3\u30d7\u30ed\u30fc\u30c9: SKILL.md \u3092\u542b\u3080 ZIP \u3092\u767b\u9332\uff08\u5358\u4e00\u30eb\u30fc\u30c8\u30d5\u30a9\u30eb\u30c0\u3001name/description \u5fc5\u9808\uff09\n"
    "- Git \u9023\u643a: \u30ea\u30dd\u30b8\u30c8\u30ea\u3092\u767b\u9332\u3057\u3066\u540c\u671f\u3057\u3001SKILL.md \u3092\u53d6\u308a\u8fbc\u3080\n"
    "- \u8a73\u7d30: Markdown \u30d7\u30ec\u30d3\u30e5\u30fc\u3001\u7de8\u96c6\u3001ZIP \u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u3001\u5171\u6709\u30ea\u30f3\u30af\n"
    "- \u30c6\u30b9\u30c8: /tests \u3067\u30d0\u30c3\u30af\u30a8\u30f3\u30c9 pytest \u3092\u5b9f\u884c\n"
)


def _truncate(text: str | None, limit: int = 400) -> str:
    if not text:
        return ""
    text = text.strip()
    return text if len(text) <= limit else text[: limit - 1] + "\u2026"


def find_relevant_skills(db: Session, question: str, *, limit: int = 5) -> list[Skill]:
    q = (question or "").strip()
    if not q:
        return []

    tokens = [t for t in q.replace("\u3000", " ").split() if len(t) >= 2][:6]
    if not tokens:
        tokens = [q[:40]]

    filters = []
    for token in tokens:
        pattern = f"%{token}%"
        tag_subq = select(SkillTag.skill_id).where(SkillTag.tag.ilike(pattern))
        filters.append(
            or_(
                Skill.name.ilike(pattern),
                Skill.description.ilike(pattern),
                Skill.category.ilike(pattern),
                Skill.author.ilike(pattern),
                Skill.skill_md_content.ilike(pattern),
                Skill.id.in_(tag_subq),
            )
        )

    stmt = (
        select(Skill)
        .options(selectinload(Skill.tags))
        .where(or_(*filters))
        .order_by(Skill.updated_at.desc())
        .limit(limit)
    )
    return list(db.scalars(stmt).all())


def _skill_context(skills: list[Skill]) -> str:
    if not skills:
        return "\uff08\u95a2\u9023 Skill \u306f\u898b\u3064\u304b\u308a\u307e\u305b\u3093\u3067\u3057\u305f\uff09"
    blocks: list[str] = []
    for skill in skills:
        tags = ", ".join(t.tag for t in skill.tags) or "-"
        blocks.append(
            "\n".join(
                [
                    f"## {skill.name}",
                    f"- id: {skill.id}",
                    f"- category: {skill.category or '-'}",
                    f"- version: {skill.version or '-'}",
                    f"- tags: {tags}",
                    f"- description: {_truncate(skill.description)}",
                    f"- body: {_truncate(skill.skill_md_content, 600)}",
                ]
            )
        )
    return "\n\n".join(blocks)


def build_fallback_answer(question: str, skills: list[Skill]) -> str:
    howto_hints = (
        "\u4f7f\u3044\u65b9",
        "\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9",
        "Git",
        "\u767b\u9332",
        "\u691c\u7d22",
        "\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9",
        "\u624b\u9806",
    )
    lines: list[str] = []
    if any(h.lower() in question.lower() or h in question for h in howto_hints):
        lines.append(
            "\u30ab\u30bf\u30ed\u30b0\u306e\u57fa\u672c\u64cd\u4f5c\u306f\u6b21\u306e\u3068\u304a\u308a\u3067\u3059\u3002"
            "\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u753b\u9762\u3067 ZIP \u767b\u9332\u3001Git \u9023\u643a\u753b\u9762\u3067\u30ea\u30dd\u30b8\u30c8\u30ea\u540c\u671f\u3001"
            "\u30ab\u30bf\u30ed\u30b0\u753b\u9762\u3067\u691c\u7d22\u30fb\u7d5e\u308a\u8fbc\u307f\u304c\u3067\u304d\u307e\u3059\u3002"
        )
    if skills:
        lines.append("\u95a2\u9023\u3057\u305d\u3046\u306a Skill \u304c\u898b\u3064\u304b\u308a\u307e\u3057\u305f:")
        for skill in skills:
            desc = _truncate(skill.description, 120) or "\u8aac\u660e\u306a\u3057"
            lines.append(f"- {skill.name}: {desc}")
        lines.append(
            "\u8a73\u7d30\u306f\u5404 Skill \u306e\u8a73\u7d30\u30da\u30fc\u30b8\u3067\u78ba\u8a8d\u3057\u3066\u304f\u3060\u3055\u3044\u3002"
        )
    else:
        lines.append(
            "\u30ab\u30bf\u30ed\u30b0\u5185\u306b\u76f4\u63a5\u4e00\u81f4\u3059\u308b Skill \u306f\u898b\u3064\u304b\u308a\u307e\u305b\u3093\u3067\u3057\u305f\u3002"
            "\u30ad\u30fc\u30ef\u30fc\u30c9\u3092\u5909\u3048\u3066\u691c\u7d22\u3059\u308b\u304b\u3001ZIP / Git \u304b\u3089\u767b\u9332\u3057\u3066\u304f\u3060\u3055\u3044\u3002"
        )
    if not lines:
        lines.append(
            "\u3054\u8cea\u554f\u5185\u5bb9\u3092\u3082\u3046\u5c11\u3057\u5177\u4f53\u7684\u306b\u6559\u3048\u3066\u304f\u3060\u3055\u3044\u3002"
        )
    return "\n".join(lines)


def call_openai(*, settings: Settings, question: str, skills: list[Skill]) -> str:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    user_content = (
        f"\u554f\u3044\u5408\u308f\u305b:\n{question}\n\n"
        f"{CATALOG_HOWTO}\n\n"
        f"# \u95a2\u9023 Skill\n{_skill_context(skills)}\n"
    )
    payload = {
        "model": settings.openai_model,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    }
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    with httpx.Client(timeout=settings.openai_timeout_sec) as client:
        response = client.post(
            f"{settings.openai_base_url.rstrip('/')}/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
    try:
        return str(data["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("Unexpected OpenAI response") from exc


def answer_inquiry(db: Session, settings: Settings, question: str) -> dict[str, Any]:
    cleaned = (question or "").strip()
    if not cleaned:
        return {
            "answer": "\u8cea\u554f\u3092\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
            "mode": "empty",
            "skills": [],
        }

    skills = find_relevant_skills(db, cleaned, limit=5)
    refs = [
        {
            "id": s.id,
            "name": s.name,
            "description": _truncate(s.description, 160),
            "category": s.category,
            "tags": [t.tag for t in s.tags],
        }
        for s in skills
    ]

    if settings.openai_api_key:
        try:
            answer = call_openai(settings=settings, question=cleaned, skills=skills)
            return {"answer": answer, "mode": "openai", "skills": refs}
        except Exception as exc:
            logger.warning("OpenAI inquiry failed: %s", exc)
            fallback = build_fallback_answer(cleaned, skills)
            return {
                "answer": fallback
                + "\n\n\uff08OpenAI \u3078\u306e\u63a5\u7d9a\u306b\u5931\u6557\u3057\u305f\u305f\u3081\u3001\u30ab\u30bf\u30ed\u30b0\u691c\u7d22\u30d9\u30fc\u30b9\u306e\u56de\u7b54\u3067\u3059\uff09",
                "mode": "fallback",
                "skills": refs,
                "error": str(exc)[:300],
            }

    return {
        "answer": build_fallback_answer(cleaned, skills)
        + "\n\n\uff08OPENAI_API_KEY \u672a\u8a2d\u5b9a\u306e\u305f\u3081\u3001\u30ab\u30bf\u30ed\u30b0\u691c\u7d22\u30d9\u30fc\u30b9\u306e\u56de\u7b54\u3067\u3059\uff09",
        "mode": "fallback",
        "skills": refs,
    }
'''

# SRC uses \u escapes in a normal string... wait, SRC is raw. Write as-is so
# inquiry.py contains \uXXXX sequences that Python interprets at import time.
OUT.write_text(SRC.lstrip("\n"), encoding="utf-8", newline="\n")
print(f"wrote {OUT}")
