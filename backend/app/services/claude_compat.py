"""Claude / Agent Skills compatibility checks for SKILL.md packages."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

from app import messages as msg

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESERVED_NAMES = frozenset({"claude", "anthropic"})
NAME_MAX = 64
DESCRIPTION_MAX = 1024
DESCRIPTION_CLAUDE_AI_MAX = 200


@dataclass
class CompatIssue:
    code: str
    severity: str  # error | warn | info
    message: str


@dataclass
class ClaudeCompatReport:
    compatible: bool
    status: str  # ok | warn | error
    summary: str
    issues: list[CompatIssue] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "compatible": self.compatible,
            "status": self.status,
            "summary": self.summary,
            "issues": [asdict(i) for i in self.issues],
        }


def _folder_from_skill_md_path(skill_md_path: str | None) -> str | None:
    if not skill_md_path:
        return None
    parts = skill_md_path.replace("\\", "/").split("/")
    if len(parts) >= 2:
        return parts[-2]
    return None


def assess_claude_compatibility(
    *,
    frontmatter_name: str | None,
    description: str | None,
    folder_name: str | None = None,
    has_frontmatter: bool = True,
    folder_required: bool = True,
) -> ClaudeCompatReport:
    """Evaluate Agent Skills / Claude loading rules.

    Compatible means no errors (warnings/info are allowed). Unknown
    frontmatter keys are ignored by compliant runtimes.
    """
    issues: list[CompatIssue] = []
    name = (frontmatter_name or "").strip()
    desc = (description or "").strip() if description is not None else ""

    if not has_frontmatter:
        issues.append(
            CompatIssue(
                code="missing_frontmatter",
                severity="error",
                message=msg.compat_missing_frontmatter(),
            )
        )

    if not name:
        issues.append(
            CompatIssue(
                code="name_missing",
                severity="error",
                message=msg.compat_name_missing(),
            )
        )
    else:
        if len(name) > NAME_MAX:
            issues.append(
                CompatIssue(
                    code="name_too_long",
                    severity="error",
                    message=msg.compat_name_too_long(len(name), NAME_MAX),
                )
            )
        if not NAME_RE.fullmatch(name):
            issues.append(
                CompatIssue(
                    code="name_invalid",
                    severity="error",
                    message=msg.compat_name_invalid(),
                )
            )
        if name in RESERVED_NAMES:
            issues.append(
                CompatIssue(
                    code="name_reserved",
                    severity="error",
                    message=msg.compat_name_reserved(name),
                )
            )

    if has_frontmatter:
        if not desc:
            issues.append(
                CompatIssue(
                    code="description_missing",
                    severity="error",
                    message=msg.compat_description_missing(),
                )
            )
        elif len(desc) > DESCRIPTION_MAX:
            issues.append(
                CompatIssue(
                    code="description_too_long",
                    severity="error",
                    message=msg.compat_description_too_long(len(desc), DESCRIPTION_MAX),
                )
            )
        elif len(desc) > DESCRIPTION_CLAUDE_AI_MAX:
            issues.append(
                CompatIssue(
                    code="description_claude_ai_limit",
                    severity="warn",
                    message=msg.compat_description_claude_ai(
                        len(desc), DESCRIPTION_CLAUDE_AI_MAX
                    ),
                )
            )

    if folder_name and name:
        if folder_name != name:
            issues.append(
                CompatIssue(
                    code="folder_name_mismatch",
                    severity="error",
                    message=msg.compat_folder_mismatch(folder_name, name),
                )
            )
    elif name and folder_required and folder_name is None:
        issues.append(
            CompatIssue(
                code="folder_name_unknown",
                severity="info",
                message=msg.compat_folder_unknown(),
            )
        )

    errors = [i for i in issues if i.severity == "error"]
    warns = [i for i in issues if i.severity == "warn"]
    if errors:
        status = "error"
        compatible = False
        summary = msg.compat_summary_error(len(errors))
    elif warns:
        status = "warn"
        compatible = True
        summary = msg.compat_summary_warn(len(warns))
    else:
        status = "ok"
        compatible = True
        summary = msg.compat_summary_ok()

    return ClaudeCompatReport(
        compatible=compatible,
        status=status,
        summary=summary,
        issues=issues,
    )


def assess_from_parsed(
    parsed: dict,
    *,
    skill_md_path: str | None = None,
    folder_name: str | None = None,
) -> dict:
    folder = folder_name or _folder_from_skill_md_path(skill_md_path)
    raw = parsed.get("skill_md_content") or ""
    has_fm = bool(raw.lstrip().startswith("---"))
    fm_name = parsed.get("frontmatter_name")
    if fm_name is None and has_fm:
        fm_name = parsed.get("name")
    report = assess_claude_compatibility(
        frontmatter_name=fm_name if isinstance(fm_name, str) else None,
        description=parsed.get("description") if has_fm else None,
        folder_name=folder,
        has_frontmatter=has_fm,
        folder_required=True,
    )
    return report.to_dict()


def assess_skill_record(
    *,
    skill_md_content: str | None,
    package_dir: str | None = None,
    git_path: str | None = None,
) -> dict:
    from app.services.skill_parser import parse_skill_markdown

    content = skill_md_content or ""
    has_fm = bool(content.lstrip().startswith("---"))
    folder = package_dir
    if not folder and git_path:
        folder = git_path.replace("\\", "/").rstrip("/").split("/")[-1] or None

    if not content:
        return assess_claude_compatibility(
            frontmatter_name=None,
            description=None,
            folder_name=folder,
            has_frontmatter=False,
        ).to_dict()

    parsed = parse_skill_markdown(content)
    if not has_fm:
        return assess_claude_compatibility(
            frontmatter_name=None,
            description=None,
            folder_name=folder,
            has_frontmatter=False,
        ).to_dict()

    return assess_claude_compatibility(
        frontmatter_name=parsed.get("frontmatter_name") or parsed.get("name"),
        description=parsed.get("description"),
        folder_name=folder,
        has_frontmatter=True,
        folder_required=True,
    ).to_dict()
