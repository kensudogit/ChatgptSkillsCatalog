"use client";

import { useEffect, useRef, useState } from "react";

const copy = {
  trigger: "利用手順",
  scroll: "スクロールして確認",
  close: "利用手順を閉じる",
  title: "Skills Catalog 利用ガイド",
  lead:
    "社内の ChatGPT / Claude / Cursor Skills を、ZIP または Git リポジトリから登録し、検索・確認・共有・ダウンロードするためのカタログです。",
  architecture:
    "Next.js から FastAPI を呼び出し、メタデータを PostgreSQL に保存します。ZIP は開発環境ではローカル、本番（ECS / Railway）では S3 またはボリュームに保管できます。",
  caution: "運用上の注意",
  claudeTitle: "Claude / Agent Skills 互換",
  claudeLead:
    "登録された Skill は Agent Skills 仕様で Claude 互換性を自動判定します。一覧のバッジと詳細画面の指摘リストで確認できます。",
  deployTitle: "デプロイと CI/CD",
  deployLead:
    "GitHub Actions で自動テストとデプロイを実行します。main への push で CI が動き、ECS へのデプロイは手動実行または有効化時に走ります。",
};

const techTags = [
  "Next.js 15",
  "React 19",
  "TypeScript",
  "FastAPI",
  "PostgreSQL",
  "Docker",
  "GitHub Actions",
  "Railway / ECS",
  "Claude Compat",
  "Git Sync",
];

const architectureItems = [
  "Next.js - 一覧・検索・アップロード・詳細・Git 連携",
  "FastAPI - Skill CRUD・ZIP 解析・ダウンロード・Git 同期・Claude 互換判定",
  "PostgreSQL - Skill・タグ・Git ソース情報",
  "Docker / Railway / ECS - 開発環境と本番実行環境",
  "GitHub Actions - CI（テスト・ビルド）と ECS への CD",
];

const steps = [
  {
    number: "01",
    title: "カタログを検索する",
    description:
      "トップ画面の検索欄に名前・説明・タグを入力します。カテゴリ、タグ、登録元（アップロード / Git 連携）、並び順、Claude 判定で絞り込めます。/ キーで検索欄にフォーカスできます。",
    note:
      "カード上の Claude バッジで互換 / 注意 / 非互換を確認できます。タグバッジをクリックするとそのタグで絞り込めます。",
  },
  {
    number: "02",
    title: "ZIP から Skill を登録する",
    description:
      "アップロード画面を開き、SKILL.md を含む ZIP をドラッグ＆ドロップします。YAML frontmatter の name / description などは自動で読み取られます。",
    note:
      "名前・説明・カテゴリ・作者・バージョン・タグは登録時に上書きできます。ファイル上限は 50MB です。サンプルは samples/sample-pcb-checklist.zip を利用できます。",
  },
  {
    number: "03",
    title: "Git リポジトリを連携する",
    description:
      "Git 連携画面で表示名、リポジトリ URL、ブランチを登録します。必要に応じて Skills サブディレクトリとアクセストークンを指定します。",
    note:
      "同期を実行すると SKILL.md を再帰検索し、新規登録・更新・削除を反映します。スキップされたパスと理由も画面上で確認できます。",
  },
  {
    number: "04",
    title: "詳細を確認・編集・共有する",
    description:
      "詳細画面で Markdown プレビュー（または原文）、メタデータ、Claude 互換性を確認します。編集で名前・説明・タグなどを更新できます。",
    note:
      "「共有リンクをコピー」で URL を共有できます。「ZIP をダウンロード」で ChatGPT / Claude / Cursor へ取り込めるパッケージを取得できます。",
  },
  {
    number: "05",
    title: "変更をデプロイする",
    description:
      "main へ push すると CI がバックエンドテスト、フロントエンドの型チェックとビルド、Docker イメージビルドを実行します。",
    note:
      "ECS へのデプロイは Actions タブの Deploy ECS を手動実行するか、リポジトリ変数 ENABLE_ECS_DEPLOY を true にして自動化します。",
  },
];

const claudeRules = [
  "frontmatter の name は小文字英数字とハイフンのみ（64 文字以内）",
  "description は必須（1024 文字以内。Claude.ai へのアップロードは 200 文字以内推奨）",
  "ZIP 内の親フォルダ名は name と完全一致させる（Claude で必須）",
  "version / author / category / tags はカタログ用メタです。Agent Skills 仕様では metadata: 配下も可",
];

const deployItems = [
  "CI - バックエンド pytest、フロントエンド型チェックとビルド、Docker イメージビルド",
  "CD - ECR へイメージを push し、ECS サービスを更新",
  "Railway - ルート Dockerfile の単一コンテナで 1 つの URL で公開",
  "有効化には ENABLE_ECS_DEPLOY と AWS 認証情報（OIDC 推奨）の設定が必要",
];

const cautions = [
  "機密情報や認証情報を SKILL.md や ZIP に含めないでください。",
  "プライベート Git のトークンは必要最小限の権限にしてください。",
  "共有・ダウンロード前に作者・バージョン・Claude 互換性・手順内容を確認してください。",
  "Claude で使う場合は、非互換バッジが付いた Skill のまま配布しないでください。",
  "本番デプロイは CI が成功したコミットを対象にしてください。",
];

export default function UsageGuide() {
  const [open, setOpen] = useState(false);
  const closeButtonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!open) return;

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    closeButtonRef.current?.focus();

    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", closeOnEscape);

    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener("keydown", closeOnEscape);
    };
  }, [open]);

  return (
    <>
      <button
        className="guide-trigger"
        type="button"
        onClick={() => setOpen(true)}
        aria-haspopup="dialog"
      >
        <span className="guide-trigger-mark" aria-hidden="true" />
        {copy.trigger}
      </button>

      {open && (
        <div
          className="guide-overlay"
          role="presentation"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) setOpen(false);
          }}
        >
          <section
            className="guide-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="usage-guide-title"
          >
            <header className="guide-header">
              <div className="guide-heading">
                <span className="guide-menu-icon" aria-hidden="true">
                  <i />
                  <i />
                  <i />
                </span>
                <div>
                  <h2 id="usage-guide-title">{copy.trigger}</h2>
                  <p>SKILLS CATALOG GUIDE</p>
                </div>
              </div>
              <span className="guide-drag-label">{copy.scroll}</span>
              <button
                ref={closeButtonRef}
                className="guide-close"
                type="button"
                onClick={() => setOpen(false)}
                aria-label={copy.close}
              >
                x
              </button>
            </header>

            <div className="guide-content">
              <section className="guide-hero">
                <p className="guide-eyebrow">CHATGPT / CLAUDE / CURSOR SKILLS</p>
                <h3>{copy.title}</h3>
                <p className="guide-lead">{copy.lead}</p>
                <div className="guide-tags">
                  {techTags.map((tag) => (
                    <span key={tag}>{tag}</span>
                  ))}
                </div>
              </section>

              <section className="guide-architecture">
                <div className="guide-section-title">
                  <span>ARCHITECTURE</span>
                  <strong>Next.js UI + FastAPI Skills API</strong>
                </div>
                <p>{copy.architecture}</p>
                <ul>
                  {architectureItems.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </section>

              <section className="guide-steps" aria-label="Basic workflow">
                <p className="guide-subheading">BASIC WORKFLOW</p>
                {steps.map((step) => (
                  <article className="guide-step" key={step.number}>
                    <div className="guide-step-number">{step.number}</div>
                    <div>
                      <h4>{step.title}</h4>
                      <p>{step.description}</p>
                      <div className="guide-note">{step.note}</div>
                    </div>
                  </article>
                ))}
              </section>

              <section className="guide-architecture">
                <div className="guide-section-title">
                  <span>COMPATIBILITY</span>
                  <strong>{copy.claudeTitle}</strong>
                </div>
                <p>{copy.claudeLead}</p>
                <ul>
                  {claudeRules.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </section>

              <section className="guide-format">
                <p className="guide-subheading">ZIP PACKAGE FORMAT</p>
                <pre>{`pcb-design-review/
|- SKILL.md       # required (folder name == name)
|- references/    # optional
+- scripts/       # optional`}</pre>
                <div className="guide-code-caption">SKILL.md frontmatter (Claude compatible)</div>
                <pre>{`---
name: pcb-design-review
description: PCB design review checklist for electronics manufacturing. Use when reviewing board layouts.
metadata:
  version: "1.0.0"
  author: design-team
  category: design-review
tags: [pcb, review, quality]
---`}</pre>
              </section>

              <section className="guide-architecture">
                <div className="guide-section-title">
                  <span>DEPLOY</span>
                  <strong>{copy.deployTitle}</strong>
                </div>
                <p>{copy.deployLead}</p>
                <ul>
                  {deployItems.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </section>

              <section className="guide-format">
                <p className="guide-subheading">CI / CD PIPELINE</p>
                <pre>{`push / pull_request  ->  .github/workflows/ci.yml
  |- backend    pytest
  |- frontend   tsc --noEmit + next build
  +- docker     backend / frontend / combined image

Deploy ECS  ->  .github/workflows/deploy-ecs.yml
  |- trigger    workflow_dispatch, or push when ENABLE_ECS_DEPLOY=true
  |- build      push images to ECR (tag = commit sha)
  +- release    render task definition -> ECS update -> wait stability`}</pre>
              </section>

              <section className="guide-topology">
                <p className="guide-subheading">SERVICE TOPOLOGY</p>
                <pre>{`Browser
  |- /              Catalog, Search, Claude filter
  |- /upload        ZIP Registration
  |- /git           Repository Sync
  +- /skills/:id    Detail / Edit / Download / Share
         |
         v
FastAPI :8000 -- PostgreSQL :5432
         |------ Local Volume / S3
         +------ Git Repository`}</pre>
              </section>

              <section className="guide-caution">
                <strong>{copy.caution}</strong>
                <ul>
                  {cautions.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </section>
            </div>
          </section>
        </div>
      )}
    </>
  );
}
