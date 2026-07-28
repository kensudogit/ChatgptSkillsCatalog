"""Japanese messages returned to the UI."""

SKILL_NOT_FOUND = "Skill が見つかりません"
GIT_SOURCE_NOT_FOUND = "Git 連携先が見つかりません"
REPOSITORY_ALREADY_REGISTERED = (
    "このリポジトリ URL は既に登録されています"
)
ZIP_REQUIRED = "ZIP ファイルをアップロードしてください"
SKILL_MD_NOT_FOUND_IN_ZIP = "ZIP 内に SKILL.md が見つかりません"
INVALID_ZIP = "ZIP ファイルとして読み込めません"
QUERY_SEARCH = "名前・説明・作者・タグの横断検索"
QUERY_TAGS = "タグ（カンマ区切り）"
DOWNLOAD_NOT_AVAILABLE = (
    "ダウンロードできるファイルがありません"
)


def file_too_large(limit_mb: int) -> str:
    return (
        "ファイルサイズが上限"
        f"（{limit_mb}MB）を超えています"
    )


def skill_md_missing(path: object) -> str:
    return f"SKILL.md が見つかりません: {path}"


def subdir_missing(subdir: str) -> str:
    return (
        "指定したサブディレクトリが"
        f"存在しません: {subdir}"
    )


def sync_summary(imported: int, updated: int, skipped: int, commit: str) -> str:
    return (
        f"新規 {imported} 件 / 更新 {updated} 件 / "
        f"スキップ {skipped} 件（commit {commit[:8]}）"
    )
