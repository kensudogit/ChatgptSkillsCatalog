"use client";

import { useEffect, useRef, useState } from "react";

const copy = {
  trigger: "利用手順",
  scroll: "スクロールして確認",
  close: "利用手順を閉じる",
  title: "Skills Catalog 利用ガイド",
  lead:
    "社内の ChatGPT Skills を、ZIP または Git リポジトリから登録し、検索・確認・共有するためのカタログです。",
  architecture:
    "フロントエンドから FastAPI を呼び出し、メタデータを PostgreSQL に保存します。ZIP は開発環境ではローカル、本番 ECS では S3 に保管できます。",
  caution: "運用上の注意",
};

const techTags = [
  "Next.js 15",
  "React 19",
  "TypeScript",
  "FastAPI",
  "PostgreSQL",
  "Docker",
  "AWS ECS",
  "Git Sync",
];

const architectureItems = [
  "Next.js - 一覧・検索・アップロード・詳細・Git 連携",
  "FastAPI - Skill CRUD・ZIP 解析・Git 同期",
  "PostgreSQL - Skill・タグ・Git ソース情報",
  "Docker / ECS - 開発環境と AWS 本番実行環境",
];

const steps = [
  {
    number: "01",
    title: "カタログを検索する",
    description:
      "トップ画面の検索欄に名前・説明・タグを入力します。カテゴリと登録元（アップロード / Git 連携）を組み合わせて絞り込めます。",
    note:
      "カードを選択すると、SKILL.md の内容・作者・バージョン・タグ・更新日時を確認できます。",
  },
  {
    number: "02",
    title: "ZIP から Skill を登録する",
    description:
      "アップロード画面を開き、SKILL.md を含む ZIP ファイルをドラッグ＆ドロップします。YAML frontmatter の情報は自動で読み取られます。",
    note:
      "名前・説明・カテゴリ・作者・バージョン・タグは登録時に上書きできます。ファイル上限は 50MB です。",
  },
  {
    number: "03",
    title: "Git リポジトリを連携する",
    description:
      "Git 連携画面で表示名、リポジトリ URL、ブランチを登録します。必要に応じて Skills のサブディレクトリとアクセストークンを指定します。",
    note:
      "同期を実行すると SKILL.md を再帰検索し、新規登録・既存 Skill の更新・削除状態の反映を行います。",
  },
  {
    number: "04",
    title: "内容を確認・共有する",
    description:
      "詳細画面で手順本文とメタデータを確認します。共有時はブラウザの詳細画面 URL を社内メンバーへ案内してください。",
    note:
      "不要になった Skill は詳細画面から削除できます。Git 由来の Skill は次回同期でも状態が更新されます。",
  },
];

const cautions = [
  "機密情報や認証情報を SKILL.md や ZIP に含めないでください。",
  "プライベート Git のトークンは必要最小限の権限にしてください。",
  "共有前に作者・バージョン・手順内容を確認してください。",
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
                <p className="guide-eyebrow">CHATGPT SKILLS PLATFORM</p>
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

              <section className="guide-format">
                <p className="guide-subheading">ZIP PACKAGE FORMAT</p>
                <pre>{`my-skill/
|- SKILL.md       # required
|- references/    # optional
\\- scripts/       # optional`}</pre>
                <div className="guide-code-caption">SKILL.md frontmatter</div>
                <pre>{`---
name: pcb-design-review
description: PCB design review support
version: 1.0.0
author: design-team
category: design-review
tags: [pcb, review]
---`}</pre>
              </section>

              <section className="guide-topology">
                <p className="guide-subheading">SERVICE TOPOLOGY</p>
                <pre>{`Browser
  |- /              Catalog & Search
  |- /upload        ZIP Registration
  |- /git           Repository Sync
  \\- /skills/:id    Skill Detail
         |
         v
FastAPI :8000 -- PostgreSQL :5432
         |------ Local Volume / S3
         \\------ Git Repository`}</pre>
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
