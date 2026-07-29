"""Rewrite UsageGuide.tsx with up-to-date Japanese content as UTF-8.

This generator stays pure ASCII: Japanese is written as \\uXXXX escapes and
decoded before writing, which avoids the CP1252 mangling that plain editors
hit on this Windows setup.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "frontend" / "src" / "components" / "UsageGuide.tsx"

CONTENT = r'''"use client";

import { useEffect, useRef, useState } from "react";

const copy = {
  trigger: "\u5229\u7528\u624b\u9806",
  scroll: "\u30b9\u30af\u30ed\u30fc\u30eb\u3057\u3066\u78ba\u8a8d",
  close: "\u5229\u7528\u624b\u9806\u3092\u9589\u3058\u308b",
  title: "Skills Catalog \u5229\u7528\u30ac\u30a4\u30c9",
  lead:
    "\u793e\u5185\u306e ChatGPT / Claude / Cursor Skills \u3092\u3001ZIP \u307e\u305f\u306f Git \u30ea\u30dd\u30b8\u30c8\u30ea\u304b\u3089\u767b\u9332\u3057\u3001\u691c\u7d22\u30fb\u78ba\u8a8d\u30fb\u5171\u6709\u30fb\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u3059\u308b\u305f\u3081\u306e\u30ab\u30bf\u30ed\u30b0\u3067\u3059\u3002",
  architecture:
    "Next.js \u304b\u3089 FastAPI \u3092\u547c\u3073\u51fa\u3057\u3001\u30e1\u30bf\u30c7\u30fc\u30bf\u3092 PostgreSQL \u306b\u4fdd\u5b58\u3057\u307e\u3059\u3002ZIP \u306f\u958b\u767a\u74b0\u5883\u3067\u306f\u30ed\u30fc\u30ab\u30eb\u3001\u672c\u756a\uff08ECS / Railway\uff09\u3067\u306f S3 \u307e\u305f\u306f\u30dc\u30ea\u30e5\u30fc\u30e0\u306b\u4fdd\u7ba1\u3067\u304d\u307e\u3059\u3002",
  caution: "\u904b\u7528\u4e0a\u306e\u6ce8\u610f",
  claudeTitle: "Claude / Agent Skills \u4e92\u63db",
  claudeLead:
    "\u767b\u9332\u3055\u308c\u305f Skill \u306f Agent Skills \u4ed5\u69d8\u3067 Claude \u4e92\u63db\u6027\u3092\u81ea\u52d5\u5224\u5b9a\u3057\u307e\u3059\u3002\u4e00\u89a7\u306e\u30d0\u30c3\u30b8\u3068\u8a73\u7d30\u753b\u9762\u306e\u6307\u6458\u30ea\u30b9\u30c8\u3067\u78ba\u8a8d\u3067\u304d\u307e\u3059\u3002",
  deployTitle: "\u30c7\u30d7\u30ed\u30a4\u3068 CI/CD",
  deployLead:
    "GitHub Actions \u3067\u81ea\u52d5\u30c6\u30b9\u30c8\u3068\u30c7\u30d7\u30ed\u30a4\u3092\u5b9f\u884c\u3057\u307e\u3059\u3002main \u3078\u306e push \u3067 CI \u304c\u52d5\u304d\u3001ECS \u3078\u306e\u30c7\u30d7\u30ed\u30a4\u306f\u624b\u52d5\u5b9f\u884c\u307e\u305f\u306f\u6709\u52b9\u5316\u6642\u306b\u8d70\u308a\u307e\u3059\u3002",
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
  "Next.js - \u4e00\u89a7\u30fb\u691c\u7d22\u30fb\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u30fb\u8a73\u7d30\u30fbGit \u9023\u643a",
  "FastAPI - Skill CRUD\u30fbZIP \u89e3\u6790\u30fb\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u30fbGit \u540c\u671f\u30fbClaude \u4e92\u63db\u5224\u5b9a",
  "PostgreSQL - Skill\u30fb\u30bf\u30b0\u30fbGit \u30bd\u30fc\u30b9\u60c5\u5831",
  "Docker / Railway / ECS - \u958b\u767a\u74b0\u5883\u3068\u672c\u756a\u5b9f\u884c\u74b0\u5883",
  "GitHub Actions - CI\uff08\u30c6\u30b9\u30c8\u30fb\u30d3\u30eb\u30c9\uff09\u3068 ECS \u3078\u306e CD",
];

const steps = [
  {
    number: "01",
    title: "\u30ab\u30bf\u30ed\u30b0\u3092\u691c\u7d22\u3059\u308b",
    description:
      "\u30c8\u30c3\u30d7\u753b\u9762\u306e\u691c\u7d22\u6b04\u306b\u540d\u524d\u30fb\u8aac\u660e\u30fb\u30bf\u30b0\u3092\u5165\u529b\u3057\u307e\u3059\u3002\u30ab\u30c6\u30b4\u30ea\u3001\u30bf\u30b0\u3001\u767b\u9332\u5143\uff08\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9 / Git \u9023\u643a\uff09\u3001\u4e26\u3073\u9806\u3001Claude \u5224\u5b9a\u3067\u7d5e\u308a\u8fbc\u3081\u307e\u3059\u3002/ \u30ad\u30fc\u3067\u691c\u7d22\u6b04\u306b\u30d5\u30a9\u30fc\u30ab\u30b9\u3067\u304d\u307e\u3059\u3002",
    note:
      "\u30ab\u30fc\u30c9\u4e0a\u306e Claude \u30d0\u30c3\u30b8\u3067\u4e92\u63db / \u6ce8\u610f / \u975e\u4e92\u63db\u3092\u78ba\u8a8d\u3067\u304d\u307e\u3059\u3002\u30bf\u30b0\u30d0\u30c3\u30b8\u3092\u30af\u30ea\u30c3\u30af\u3059\u308b\u3068\u305d\u306e\u30bf\u30b0\u3067\u7d5e\u308a\u8fbc\u3081\u307e\u3059\u3002",
  },
  {
    number: "02",
    title: "ZIP \u304b\u3089 Skill \u3092\u767b\u9332\u3059\u308b",
    description:
      "\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u753b\u9762\u3092\u958b\u304d\u3001SKILL.md \u3092\u542b\u3080 ZIP \u3092\u30c9\u30e9\u30c3\u30b0\uff06\u30c9\u30ed\u30c3\u30d7\u3057\u307e\u3059\u3002YAML frontmatter \u306e name / description \u306a\u3069\u306f\u81ea\u52d5\u3067\u8aad\u307f\u53d6\u3089\u308c\u307e\u3059\u3002",
    note:
      "\u540d\u524d\u30fb\u8aac\u660e\u30fb\u30ab\u30c6\u30b4\u30ea\u30fb\u4f5c\u8005\u30fb\u30d0\u30fc\u30b8\u30e7\u30f3\u30fb\u30bf\u30b0\u306f\u767b\u9332\u6642\u306b\u4e0a\u66f8\u304d\u3067\u304d\u307e\u3059\u3002\u30d5\u30a1\u30a4\u30eb\u4e0a\u9650\u306f 50MB \u3067\u3059\u3002\u30b5\u30f3\u30d7\u30eb\u306f samples/sample-pcb-checklist.zip \u3092\u5229\u7528\u3067\u304d\u307e\u3059\u3002",
  },
  {
    number: "03",
    title: "Git \u30ea\u30dd\u30b8\u30c8\u30ea\u3092\u9023\u643a\u3059\u308b",
    description:
      "Git \u9023\u643a\u753b\u9762\u3067\u8868\u793a\u540d\u3001\u30ea\u30dd\u30b8\u30c8\u30ea URL\u3001\u30d6\u30e9\u30f3\u30c1\u3092\u767b\u9332\u3057\u307e\u3059\u3002\u5fc5\u8981\u306b\u5fdc\u3058\u3066 Skills \u30b5\u30d6\u30c7\u30a3\u30ec\u30af\u30c8\u30ea\u3068\u30a2\u30af\u30bb\u30b9\u30c8\u30fc\u30af\u30f3\u3092\u6307\u5b9a\u3057\u307e\u3059\u3002",
    note:
      "\u540c\u671f\u3092\u5b9f\u884c\u3059\u308b\u3068 SKILL.md \u3092\u518d\u5e30\u691c\u7d22\u3057\u3001\u65b0\u898f\u767b\u9332\u30fb\u66f4\u65b0\u30fb\u524a\u9664\u3092\u53cd\u6620\u3057\u307e\u3059\u3002\u30b9\u30ad\u30c3\u30d7\u3055\u308c\u305f\u30d1\u30b9\u3068\u7406\u7531\u3082\u753b\u9762\u4e0a\u3067\u78ba\u8a8d\u3067\u304d\u307e\u3059\u3002",
  },
  {
    number: "04",
    title: "\u8a73\u7d30\u3092\u78ba\u8a8d\u30fb\u7de8\u96c6\u30fb\u5171\u6709\u3059\u308b",
    description:
      "\u8a73\u7d30\u753b\u9762\u3067 Markdown \u30d7\u30ec\u30d3\u30e5\u30fc\uff08\u307e\u305f\u306f\u539f\u6587\uff09\u3001\u30e1\u30bf\u30c7\u30fc\u30bf\u3001Claude \u4e92\u63db\u6027\u3092\u78ba\u8a8d\u3057\u307e\u3059\u3002\u7de8\u96c6\u3067\u540d\u524d\u30fb\u8aac\u660e\u30fb\u30bf\u30b0\u306a\u3069\u3092\u66f4\u65b0\u3067\u304d\u307e\u3059\u3002",
    note:
      "\u300c\u5171\u6709\u30ea\u30f3\u30af\u3092\u30b3\u30d4\u30fc\u300d\u3067 URL \u3092\u5171\u6709\u3067\u304d\u307e\u3059\u3002\u300cZIP \u3092\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u300d\u3067 ChatGPT / Claude / Cursor \u3078\u53d6\u308a\u8fbc\u3081\u308b\u30d1\u30c3\u30b1\u30fc\u30b8\u3092\u53d6\u5f97\u3067\u304d\u307e\u3059\u3002",
  },
  {
    number: "05",
    title: "\u5909\u66f4\u3092\u30c7\u30d7\u30ed\u30a4\u3059\u308b",
    description:
      "main \u3078 push \u3059\u308b\u3068 CI \u304c\u30d0\u30c3\u30af\u30a8\u30f3\u30c9\u30c6\u30b9\u30c8\u3001\u30d5\u30ed\u30f3\u30c8\u30a8\u30f3\u30c9\u306e\u578b\u30c1\u30a7\u30c3\u30af\u3068\u30d3\u30eb\u30c9\u3001Docker \u30a4\u30e1\u30fc\u30b8\u30d3\u30eb\u30c9\u3092\u5b9f\u884c\u3057\u307e\u3059\u3002",
    note:
      "ECS \u3078\u306e\u30c7\u30d7\u30ed\u30a4\u306f Actions \u30bf\u30d6\u306e Deploy ECS \u3092\u624b\u52d5\u5b9f\u884c\u3059\u308b\u304b\u3001\u30ea\u30dd\u30b8\u30c8\u30ea\u5909\u6570 ENABLE_ECS_DEPLOY \u3092 true \u306b\u3057\u3066\u81ea\u52d5\u5316\u3057\u307e\u3059\u3002",
  },
];

const claudeRules = [
  "frontmatter \u306e name \u306f\u5c0f\u6587\u5b57\u82f1\u6570\u5b57\u3068\u30cf\u30a4\u30d5\u30f3\u306e\u307f\uff0864 \u6587\u5b57\u4ee5\u5185\uff09",
  "description \u306f\u5fc5\u9808\uff081024 \u6587\u5b57\u4ee5\u5185\u3002Claude.ai \u3078\u306e\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u306f 200 \u6587\u5b57\u4ee5\u5185\u63a8\u5968\uff09",
  "ZIP \u5185\u306e\u89aa\u30d5\u30a9\u30eb\u30c0\u540d\u306f name \u3068\u5b8c\u5168\u4e00\u81f4\u3055\u305b\u308b\uff08Claude \u3067\u5fc5\u9808\uff09",
  "version / author / category / tags \u306f\u30ab\u30bf\u30ed\u30b0\u7528\u30e1\u30bf\u3067\u3059\u3002Agent Skills \u4ed5\u69d8\u3067\u306f metadata: \u914d\u4e0b\u3082\u53ef",
];

const deployItems = [
  "CI - \u30d0\u30c3\u30af\u30a8\u30f3\u30c9 pytest\u3001\u30d5\u30ed\u30f3\u30c8\u30a8\u30f3\u30c9\u578b\u30c1\u30a7\u30c3\u30af\u3068\u30d3\u30eb\u30c9\u3001Docker \u30a4\u30e1\u30fc\u30b8\u30d3\u30eb\u30c9",
  "CD - ECR \u3078\u30a4\u30e1\u30fc\u30b8\u3092 push \u3057\u3001ECS \u30b5\u30fc\u30d3\u30b9\u3092\u66f4\u65b0",
  "Railway - \u30eb\u30fc\u30c8 Dockerfile \u306e\u5358\u4e00\u30b3\u30f3\u30c6\u30ca\u3067 1 \u3064\u306e URL \u3067\u516c\u958b",
  "\u6709\u52b9\u5316\u306b\u306f ENABLE_ECS_DEPLOY \u3068 AWS \u8a8d\u8a3c\u60c5\u5831\uff08OIDC \u63a8\u5968\uff09\u306e\u8a2d\u5b9a\u304c\u5fc5\u8981",
];

const cautions = [
  "\u6a5f\u5bc6\u60c5\u5831\u3084\u8a8d\u8a3c\u60c5\u5831\u3092 SKILL.md \u3084 ZIP \u306b\u542b\u3081\u306a\u3044\u3067\u304f\u3060\u3055\u3044\u3002",
  "\u30d7\u30e9\u30a4\u30d9\u30fc\u30c8 Git \u306e\u30c8\u30fc\u30af\u30f3\u306f\u5fc5\u8981\u6700\u5c0f\u9650\u306e\u6a29\u9650\u306b\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
  "\u5171\u6709\u30fb\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u524d\u306b\u4f5c\u8005\u30fb\u30d0\u30fc\u30b8\u30e7\u30f3\u30fbClaude \u4e92\u63db\u6027\u30fb\u624b\u9806\u5185\u5bb9\u3092\u78ba\u8a8d\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
  "Claude \u3067\u4f7f\u3046\u5834\u5408\u306f\u3001\u975e\u4e92\u63db\u30d0\u30c3\u30b8\u304c\u4ed8\u3044\u305f Skill \u306e\u307e\u307e\u914d\u5e03\u3057\u306a\u3044\u3067\u304f\u3060\u3055\u3044\u3002",
  "\u672c\u756a\u30c7\u30d7\u30ed\u30a4\u306f CI \u304c\u6210\u529f\u3057\u305f\u30b3\u30df\u30c3\u30c8\u3092\u5bfe\u8c61\u306b\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
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
'''

decoded = CONTENT.encode("ascii").decode("unicode_escape")
OUT.write_text(decoded, encoding="utf-8", newline="\n")
print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size} bytes)")

text = OUT.read_text(encoding="utf-8")
for expected in (
    "\u5229\u7528\u624b\u9806",
    "Claude / Agent Skills \u4e92\u63db",
    "\u30c7\u30d7\u30ed\u30a4\u3068 CI/CD",
    "ENABLE_ECS_DEPLOY",
):
    assert expected in text, expected
print("utf-8 ok")
