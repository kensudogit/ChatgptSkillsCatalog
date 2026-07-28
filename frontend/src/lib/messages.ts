export const messages = {
  app: {
    title: "Skills Catalog | ChatGPT Skills",
    description:
      "社内の ChatGPT Skills を登録・検索・共有するためのカタログ",
    brandSub: "社内向け",
    footer: "ChatGPT Skills Catalog - 社内限定",
  },
  nav: {
    catalog: "カタログ",
    upload: "アップロード",
    git: "Git 連携",
  },
  common: {
    loading: "読み込み中...",
    loadFailed: "読み込みに失敗しました",
    deleteFailed: "削除に失敗しました",
    noDescription: "説明なし",
    cancel: "キャンセル",
    register: "登録する",
    saving: "保存中...",
    delete: "削除",
    deleting: "削除中...",
    sourceUpload: "アップロード",
    sourceGit: "Git 連携",
  },
  catalog: {
    title: "Skills カタログ",
    lead:
      "社内の ChatGPT Skills を一元管理し、検索・共有できます。ZIP アップロードまたは Git リポジトリ連携で登録してください。",
    uploadZip: "ZIP をアップロード",
    gitSync: "Git 連携",
    searchPlaceholder: "名前・説明・タグで検索...",
    allCategories: "すべてのカテゴリ",
    allSources: "すべての登録元",
    allTags: "すべてのタグ",
    sortUpdated: "更新が新しい順",
    sortName: "名前順",
    sortCreated: "登録が新しい順",
    emptyTitle: "該当する Skill が見つかりません。",
    emptyCatalog: "まだ Skill が登録されていません。",
    emptyFiltered: "条件に一致する Skill がありません。検索条件を変更してください。",
    emptyAction: "最初の Skill を登録する",
    clearFilters: "条件をクリア",
    prev: "前へ",
    next: "次へ",
  },
  upload: {
    title: "Skill をアップロード",
    lead:
      "SKILL.md を含む ZIP ファイルを登録します。YAML frontmatter があればメタデータを自動で読み取ります。",
    requireFile: "ZIP ファイルを選択してください",
    failed: "アップロードに失敗しました",
    selected: "選択中",
    dropHint:
      "ZIP ファイルをドラッグ＆ドロップ、またはクリックして選択",
    dropNote: "SKILL.md 必須 / 最大 50MB",
    labelName: "名前（任意）",
    labelDescription: "説明（任意）",
    labelCategory: "カテゴリ",
    labelAuthor: "作者",
    labelVersion: "バージョン",
    labelTags: "タグ（カンマ区切り）",
    submitting: "アップロード中...",
  },
  git: {
    title: "Git リポジトリ連携",
    lead:
      "Skills を管理している Git リポジトリを登録し、SKILL.md を走査してカタログへ取り込みます。",
    formTitle: "連携先を登録",
    labelName: "表示名",
    placeholderName: "設計部 Skills",
    labelUrl: "リポジトリ URL",
    labelBranch: "ブランチ",
    labelSubdir: "Skills サブディレクトリ（任意）",
    labelToken:
      "アクセストークン（任意・プライベートリポジトリ用）",
    created:
      "連携先を登録しました。同期を実行すると Skills を取り込みます。",
    registerFailed: "登録に失敗しました",
    syncFailed: "同期に失敗しました",
    empty: "連携先が登録されていません。",
    thName: "名前",
    thRepo: "リポジトリ",
    thStatus: "状態",
    thSkills: "Skill 数",
    thActions: "操作",
    sync: "同期",
    syncing: "同期中...",
    tokenSet: "トークン設定済み",
  },
  detail: {
    back: "カタログへ戻る",
    metadata: "メタデータ",
    emptyBody: "（本文がありません）",
    labelSource: "登録元",
    labelCategory: "カテゴリ",
    labelVersion: "バージョン",
    labelAuthor: "作者",
    labelFilename: "ファイル名",
    labelGitPath: "Git パス",
    labelCommit: "コミット",
    labelUpdated: "更新日時",
    download: "ZIP をダウンロード",
    downloading: "ダウンロード中...",
    downloadFailed: "ダウンロードに失敗しました",
    copyLink: "共有リンクをコピー",
    copied: "リンクをコピーしました",
    copyFailed: "コピーに失敗しました",
    edit: "編集",
    save: "保存する",
    saved: "保存しました",
    saveFailed: "保存に失敗しました",
    viewRendered: "プレビュー",
    viewRaw: "原文",
  },
  gitExtras: {
    skippedTitle: "スキップされたパス",
  },
} as const;

export function sourceLabel(sourceType: string): string {
  return sourceType === "git" ? messages.common.sourceGit : messages.common.sourceUpload;
}

export function confirmDeleteMessage(name: string): string {
  return `「${name}」を削除しますか？`;
}

export function pageRangeLabel(total: number, from: number, to: number): string {
  return `全 ${total} 件中 ${from}-${to} 件を表示`;
}

export function syncSummary(
  imported: number,
  updated: number,
  skipped: number
): string {
  return `同期完了: 新規 ${imported} 件 / 更新 ${updated} 件 / スキップ ${skipped} 件`;
}

export function syncStatusLabel(status: string | null | undefined): string {
  if (status === "success") return "成功";
  if (status === "error") return "エラー";
  return "未実行";
}
