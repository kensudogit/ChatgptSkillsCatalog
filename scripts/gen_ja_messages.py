"""Generate UTF-8 message catalogs that contain Japanese literals.

Japanese text is written here as \\uXXXX escapes so this generator stays pure
ASCII; the generated files are written as real UTF-8 with LF endings.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONTEND_MESSAGES = ROOT / "frontend" / "src" / "lib" / "messages.ts"
BACKEND_MESSAGES = ROOT / "backend" / "app" / "messages.py"
USAGE_GUIDE = ROOT / "frontend" / "src" / "components" / "UsageGuide.tsx"

FRONTEND_TS = """export const messages = {
  app: {
    title: "Skills Catalog | ChatGPT Skills",
    description:
      "\u793e\u5185\u306e ChatGPT Skills \u3092\u767b\u9332\u30fb\u691c\u7d22\u30fb\u5171\u6709\u3059\u308b\u305f\u3081\u306e\u30ab\u30bf\u30ed\u30b0",
    brandSub: "\u793e\u5185\u5411\u3051",
    footer: "ChatGPT Skills Catalog - \u793e\u5185\u9650\u5b9a",
  },
  nav: {
    catalog: "\u30ab\u30bf\u30ed\u30b0",
    upload: "\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9",
    git: "Git \u9023\u643a",
  },
  common: {
    loading: "\u8aad\u307f\u8fbc\u307f\u4e2d...",
    loadFailed: "\u8aad\u307f\u8fbc\u307f\u306b\u5931\u6557\u3057\u307e\u3057\u305f",
    deleteFailed: "\u524a\u9664\u306b\u5931\u6557\u3057\u307e\u3057\u305f",
    noDescription: "\u8aac\u660e\u306a\u3057",
    cancel: "\u30ad\u30e3\u30f3\u30bb\u30eb",
    register: "\u767b\u9332\u3059\u308b",
    saving: "\u4fdd\u5b58\u4e2d...",
    delete: "\u524a\u9664",
    deleting: "\u524a\u9664\u4e2d...",
    sourceUpload: "\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9",
    sourceGit: "Git \u9023\u643a",
  },
  catalog: {
    title: "Skills \u30ab\u30bf\u30ed\u30b0",
    lead:
      "\u793e\u5185\u306e ChatGPT Skills \u3092\u4e00\u5143\u7ba1\u7406\u3057\u3001\u691c\u7d22\u30fb\u5171\u6709\u3067\u304d\u307e\u3059\u3002ZIP \u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u307e\u305f\u306f Git \u30ea\u30dd\u30b8\u30c8\u30ea\u9023\u643a\u3067\u767b\u9332\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
    uploadZip: "ZIP \u3092\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9",
    gitSync: "Git \u9023\u643a",
    searchPlaceholder: "\u540d\u524d\u30fb\u8aac\u660e\u30fb\u30bf\u30b0\u3067\u691c\u7d22...",
    allCategories: "\u3059\u3079\u3066\u306e\u30ab\u30c6\u30b4\u30ea",
    allSources: "\u3059\u3079\u3066\u306e\u767b\u9332\u5143",
    allTags: "\u3059\u3079\u3066\u306e\u30bf\u30b0",
    sortUpdated: "\u66f4\u65b0\u304c\u65b0\u3057\u3044\u9806",
    sortName: "\u540d\u524d\u9806",
    sortCreated: "\u767b\u9332\u304c\u65b0\u3057\u3044\u9806",
    emptyTitle: "\u8a72\u5f53\u3059\u308b Skill \u304c\u898b\u3064\u304b\u308a\u307e\u305b\u3093\u3002",
    emptyCatalog: "\u307e\u3060 Skill \u304c\u767b\u9332\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u3002",
    emptyFiltered: "\u6761\u4ef6\u306b\u4e00\u81f4\u3059\u308b Skill \u304c\u3042\u308a\u307e\u305b\u3093\u3002\u691c\u7d22\u6761\u4ef6\u3092\u5909\u66f4\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
    emptyAction: "\u6700\u521d\u306e Skill \u3092\u767b\u9332\u3059\u308b",
    clearFilters: "\u6761\u4ef6\u3092\u30af\u30ea\u30a2",
    prev: "\u524d\u3078",
    next: "\u6b21\u3078",
  },
  upload: {
    title: "Skill \u3092\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9",
    lead:
      "SKILL.md \u3092\u542b\u3080 ZIP \u30d5\u30a1\u30a4\u30eb\u3092\u767b\u9332\u3057\u307e\u3059\u3002YAML frontmatter \u304c\u3042\u308c\u3070\u30e1\u30bf\u30c7\u30fc\u30bf\u3092\u81ea\u52d5\u3067\u8aad\u307f\u53d6\u308a\u307e\u3059\u3002",
    requireFile: "ZIP \u30d5\u30a1\u30a4\u30eb\u3092\u9078\u629e\u3057\u3066\u304f\u3060\u3055\u3044",
    failed: "\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u306b\u5931\u6557\u3057\u307e\u3057\u305f",
    selected: "\u9078\u629e\u4e2d",
    dropHint:
      "ZIP \u30d5\u30a1\u30a4\u30eb\u3092\u30c9\u30e9\u30c3\u30b0\uff06\u30c9\u30ed\u30c3\u30d7\u3001\u307e\u305f\u306f\u30af\u30ea\u30c3\u30af\u3057\u3066\u9078\u629e",
    dropNote: "SKILL.md \u5fc5\u9808 / \u6700\u5927 50MB",
    labelName: "\u540d\u524d\uff08\u4efb\u610f\uff09",
    labelDescription: "\u8aac\u660e\uff08\u4efb\u610f\uff09",
    labelCategory: "\u30ab\u30c6\u30b4\u30ea",
    labelAuthor: "\u4f5c\u8005",
    labelVersion: "\u30d0\u30fc\u30b8\u30e7\u30f3",
    labelTags: "\u30bf\u30b0\uff08\u30ab\u30f3\u30de\u533a\u5207\u308a\uff09",
    submitting: "\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u4e2d...",
  },
  git: {
    title: "Git \u30ea\u30dd\u30b8\u30c8\u30ea\u9023\u643a",
    lead:
      "Skills \u3092\u7ba1\u7406\u3057\u3066\u3044\u308b Git \u30ea\u30dd\u30b8\u30c8\u30ea\u3092\u767b\u9332\u3057\u3001SKILL.md \u3092\u8d70\u67fb\u3057\u3066\u30ab\u30bf\u30ed\u30b0\u3078\u53d6\u308a\u8fbc\u307f\u307e\u3059\u3002",
    formTitle: "\u9023\u643a\u5148\u3092\u767b\u9332",
    labelName: "\u8868\u793a\u540d",
    placeholderName: "\u8a2d\u8a08\u90e8 Skills",
    labelUrl: "\u30ea\u30dd\u30b8\u30c8\u30ea URL",
    labelBranch: "\u30d6\u30e9\u30f3\u30c1",
    labelSubdir: "Skills \u30b5\u30d6\u30c7\u30a3\u30ec\u30af\u30c8\u30ea\uff08\u4efb\u610f\uff09",
    labelToken:
      "\u30a2\u30af\u30bb\u30b9\u30c8\u30fc\u30af\u30f3\uff08\u4efb\u610f\u30fb\u30d7\u30e9\u30a4\u30d9\u30fc\u30c8\u30ea\u30dd\u30b8\u30c8\u30ea\u7528\uff09",
    created:
      "\u9023\u643a\u5148\u3092\u767b\u9332\u3057\u307e\u3057\u305f\u3002\u540c\u671f\u3092\u5b9f\u884c\u3059\u308b\u3068 Skills \u3092\u53d6\u308a\u8fbc\u307f\u307e\u3059\u3002",
    registerFailed: "\u767b\u9332\u306b\u5931\u6557\u3057\u307e\u3057\u305f",
    syncFailed: "\u540c\u671f\u306b\u5931\u6557\u3057\u307e\u3057\u305f",
    empty: "\u9023\u643a\u5148\u304c\u767b\u9332\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u3002",
    thName: "\u540d\u524d",
    thRepo: "\u30ea\u30dd\u30b8\u30c8\u30ea",
    thStatus: "\u72b6\u614b",
    thSkills: "Skill \u6570",
    thActions: "\u64cd\u4f5c",
    sync: "\u540c\u671f",
    syncing: "\u540c\u671f\u4e2d...",
    tokenSet: "\u30c8\u30fc\u30af\u30f3\u8a2d\u5b9a\u6e08\u307f",
  },
  detail: {
    back: "\u30ab\u30bf\u30ed\u30b0\u3078\u623b\u308b",
    metadata: "\u30e1\u30bf\u30c7\u30fc\u30bf",
    emptyBody: "\uff08\u672c\u6587\u304c\u3042\u308a\u307e\u305b\u3093\uff09",
    labelSource: "\u767b\u9332\u5143",
    labelCategory: "\u30ab\u30c6\u30b4\u30ea",
    labelVersion: "\u30d0\u30fc\u30b8\u30e7\u30f3",
    labelAuthor: "\u4f5c\u8005",
    labelFilename: "\u30d5\u30a1\u30a4\u30eb\u540d",
    labelGitPath: "Git \u30d1\u30b9",
    labelCommit: "\u30b3\u30df\u30c3\u30c8",
    labelUpdated: "\u66f4\u65b0\u65e5\u6642",
    download: "ZIP \u3092\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9",
    downloading: "\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u4e2d...",
    downloadFailed: "\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u306b\u5931\u6557\u3057\u307e\u3057\u305f",
    copyLink: "\u5171\u6709\u30ea\u30f3\u30af\u3092\u30b3\u30d4\u30fc",
    copied: "\u30ea\u30f3\u30af\u3092\u30b3\u30d4\u30fc\u3057\u307e\u3057\u305f",
    copyFailed: "\u30b3\u30d4\u30fc\u306b\u5931\u6557\u3057\u307e\u3057\u305f",
    edit: "\u7de8\u96c6",
    save: "\u4fdd\u5b58\u3059\u308b",
    saved: "\u4fdd\u5b58\u3057\u307e\u3057\u305f",
    saveFailed: "\u4fdd\u5b58\u306b\u5931\u6557\u3057\u307e\u3057\u305f",
    viewRendered: "\u30d7\u30ec\u30d3\u30e5\u30fc",
    viewRaw: "\u539f\u6587",
  },
  gitExtras: {
    skippedTitle: "\u30b9\u30ad\u30c3\u30d7\u3055\u308c\u305f\u30d1\u30b9",
  },
} as const;

export function sourceLabel(sourceType: string): string {
  return sourceType === "git" ? messages.common.sourceGit : messages.common.sourceUpload;
}

export function confirmDeleteMessage(name: string): string {
  return `\u300c${name}\u300d\u3092\u524a\u9664\u3057\u307e\u3059\u304b\uff1f`;
}

export function pageRangeLabel(total: number, from: number, to: number): string {
  return `\u5168 ${total} \u4ef6\u4e2d ${from}-${to} \u4ef6\u3092\u8868\u793a`;
}

export function syncSummary(
  imported: number,
  updated: number,
  skipped: number
): string {
  return `\u540c\u671f\u5b8c\u4e86: \u65b0\u898f ${imported} \u4ef6 / \u66f4\u65b0 ${updated} \u4ef6 / \u30b9\u30ad\u30c3\u30d7 ${skipped} \u4ef6`;
}

export function syncStatusLabel(status: string | null | undefined): string {
  if (status === "success") return "\u6210\u529f";
  if (status === "error") return "\u30a8\u30e9\u30fc";
  return "\u672a\u5b9f\u884c";
}
"""

BACKEND_PY = '''"""Japanese messages returned to the UI."""

SKILL_NOT_FOUND = "Skill \u304c\u898b\u3064\u304b\u308a\u307e\u305b\u3093"
GIT_SOURCE_NOT_FOUND = "Git \u9023\u643a\u5148\u304c\u898b\u3064\u304b\u308a\u307e\u305b\u3093"
REPOSITORY_ALREADY_REGISTERED = (
    "\u3053\u306e\u30ea\u30dd\u30b8\u30c8\u30ea URL \u306f\u65e2\u306b\u767b\u9332\u3055\u308c\u3066\u3044\u307e\u3059"
)
ZIP_REQUIRED = "ZIP \u30d5\u30a1\u30a4\u30eb\u3092\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u3057\u3066\u304f\u3060\u3055\u3044"
SKILL_MD_NOT_FOUND_IN_ZIP = "ZIP \u5185\u306b SKILL.md \u304c\u898b\u3064\u304b\u308a\u307e\u305b\u3093"
INVALID_ZIP = "ZIP \u30d5\u30a1\u30a4\u30eb\u3068\u3057\u3066\u8aad\u307f\u8fbc\u3081\u307e\u305b\u3093"
QUERY_SEARCH = "\u540d\u524d\u30fb\u8aac\u660e\u30fb\u4f5c\u8005\u30fb\u30bf\u30b0\u306e\u6a2a\u65ad\u691c\u7d22"
QUERY_TAGS = "\u30bf\u30b0\uff08\u30ab\u30f3\u30de\u533a\u5207\u308a\uff09"
DOWNLOAD_NOT_AVAILABLE = (
    "\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u3067\u304d\u308b\u30d5\u30a1\u30a4\u30eb\u304c\u3042\u308a\u307e\u305b\u3093"
)


def file_too_large(limit_mb: int) -> str:
    return (
        "\u30d5\u30a1\u30a4\u30eb\u30b5\u30a4\u30ba\u304c\u4e0a\u9650"
        f"\uff08{limit_mb}MB\uff09\u3092\u8d85\u3048\u3066\u3044\u307e\u3059"
    )


def skill_md_missing(path: object) -> str:
    return f"SKILL.md \u304c\u898b\u3064\u304b\u308a\u307e\u305b\u3093: {path}"


def subdir_missing(subdir: str) -> str:
    return (
        "\u6307\u5b9a\u3057\u305f\u30b5\u30d6\u30c7\u30a3\u30ec\u30af\u30c8\u30ea\u304c"
        f"\u5b58\u5728\u3057\u307e\u305b\u3093: {subdir}"
    )


def sync_summary(imported: int, updated: int, skipped: int, commit: str) -> str:
    return (
        f"\u65b0\u898f {imported} \u4ef6 / \u66f4\u65b0 {updated} \u4ef6 / "
        f"\u30b9\u30ad\u30c3\u30d7 {skipped} \u4ef6\uff08commit {commit[:8]}\uff09"
    )
'''


# Align the guide wording with the Japanese navigation labels.
USAGE_GUIDE_REPLACEMENTS = [
    (
        "\uff08Upload / Git\uff09",
        "\uff08\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9 / Git \u9023\u643a\uff09",
    ),
    (
        "Upload \u3092\u958b\u304d\u3001",
        "\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u753b\u9762\u3092\u958b\u304d\u3001",
    ),
    (
        "Git Sync \u3067\u8868\u793a\u540d\u3001",
        "Git \u9023\u643a\u753b\u9762\u3067\u8868\u793a\u540d\u3001",
    ),
    (
        "Sync \u3092\u5b9f\u884c\u3059\u308b\u3068",
        "\u540c\u671f\u3092\u5b9f\u884c\u3059\u308b\u3068",
    ),
]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"wrote {path.relative_to(ROOT)} ({len(content.encode('utf-8'))} bytes)")


def rewrite_usage_guide(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), text)
    for old, new in USAGE_GUIDE_REPLACEMENTS:
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"rewrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    write(FRONTEND_MESSAGES, FRONTEND_TS)
    write(BACKEND_MESSAGES, BACKEND_PY)
    rewrite_usage_guide(USAGE_GUIDE)
