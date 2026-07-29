"""Japanese messages returned to the UI."""

SKILL_NOT_FOUND = "Skill が見つかりません"
GIT_SOURCE_NOT_FOUND = "Git 連携先が見つかりません"
REPOSITORY_ALREADY_REGISTERED = (
    "このリポジトリ URL は既に登録されています"
)
ZIP_REQUIRED = "ZIP ファイルをアップロードしてください"
INVALID_ZIP_EXTENSION_ONLY = (
    "拡張子が ZIP でも実体が ZIP 形式ではありません"
)
SKILL_MD_NOT_FOUND_IN_ZIP = "ZIP 内に SKILL.md が見つかりません"
MULTIPLE_SKILL_MD = "ZIP 内に SKILL.md が複数あります"
INVALID_ZIP = "ZIP ファイルとして読み込めません"
MISSING_REQUIRED_METADATA = (
    "必須メタ情報（name / description）が不足しています"
)
DUPLICATE_SKILL_VERSION = (
    "同一 Skill 名と同一バージョンが既に登録されています"
)
TOO_MANY_FILES = "ZIP 内のファイル数が上限を超えています"
UNCOMPRESSED_TOO_LARGE = (
    "展開後サイズが上限を超えています（ZIP 爆弾の可能性）"
)
COMPRESSION_RATIO_TOO_HIGH = (
    "圧縮率が異常に高いため拒否しました（ZIP 爆弾の可能性）"
)
ZIP_SLIP_DETECTED = "ZIP Slip（パストラバーサル）を検出したため拒否しました"
SYMLINK_NOT_ALLOWED = "シンボリックリンクを含む ZIP はアップロードできません"
SINGLE_ROOT_REQUIRED = (
    "ZIP は単一のルートディレクトリ配下にパッケージしてください"
)
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


def too_many_files(limit: int) -> str:
    return f"ZIP 内のファイル数が上限（{limit}）を超えています"


def uncompressed_too_large(limit_mb: int) -> str:
    return (
        "展開後サイズが上限"
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


# --- Claude / Agent Skills compatibility ---
COMPAT_OK = "Claude 互換"
COMPAT_WARN = "Claude 互換（注意）"
COMPAT_ERROR = "Claude 非互換"


def compat_summary_ok() -> str:
    return COMPAT_OK


def compat_summary_warn(count: int) -> str:
    return f"Claude 互換（注意 {count} 件）"


def compat_summary_error(count: int) -> str:
    return f"Claude 非互換（{count} 件のエラー）"


def compat_missing_frontmatter() -> str:
    return "SKILL.md 先頭に YAML frontmatter（---）がありません"


def compat_name_missing() -> str:
    return "frontmatter の name が必須です"


def compat_name_too_long(length: int, limit: int) -> str:
    return (
        f"name は {limit} 文字以内である必要があります"
        f"（現在 {length} 文字）"
    )


def compat_name_invalid() -> str:
    return (
        "name は小文字英数字とハイフンのみ"
        "（先頭・末尾のハイフン、連続ハイフン不可）"
    )


def compat_name_reserved(name: str) -> str:
    return f"name「{name}」は予約語のため使用できません"


def compat_description_missing() -> str:
    return "frontmatter の description が必須です"


def compat_description_too_long(length: int, limit: int) -> str:
    return (
        f"description は {limit} 文字以内である必要があります"
        f"（現在 {length} 文字）"
    )


def compat_description_claude_ai(length: int, limit: int) -> str:
    return (
        f"Claude.ai へのアップロードは description {limit} 文字以内推奨"
        f"（現在 {length} 文字）。Claude Code / API では問題ありません"
    )


def compat_folder_mismatch(folder: str, name: str) -> str:
    return (
        f"親フォルダ名「{folder}」が name「{name}」と一致していません。"
        "Claude では一致が必須です"
    )


def compat_folder_unknown() -> str:
    return (
        "パッケージの親フォルダ名を確認できませんでした。"
        "ZIP では name と同名フォルダ配下に置いてください"
    )
