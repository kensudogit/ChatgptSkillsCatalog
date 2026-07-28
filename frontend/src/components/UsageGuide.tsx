"use client";

import { useEffect, useRef, useState } from "react";

const copy = {
  trigger: "\u5229\u7528\u624b\u9806",
  scroll: "\u30b9\u30af\u30ed\u30fc\u30eb\u3057\u3066\u78ba\u8a8d",
  close: "\u5229\u7528\u624b\u9806\u3092\u9589\u3058\u308b",
  title: "Skills Catalog \u5229\u7528\u30ac\u30a4\u30c9",
  lead:
    "\u793e\u5185\u306e ChatGPT Skills \u3092\u3001ZIP \u307e\u305f\u306f Git \u30ea\u30dd\u30b8\u30c8\u30ea\u304b\u3089\u767b\u9332\u3057\u3001\u691c\u7d22\u30fb\u78ba\u8a8d\u30fb\u5171\u6709\u3059\u308b\u305f\u3081\u306e\u30ab\u30bf\u30ed\u30b0\u3067\u3059\u3002",
  architecture:
    "\u30d5\u30ed\u30f3\u30c8\u30a8\u30f3\u30c9\u304b\u3089 FastAPI \u3092\u547c\u3073\u51fa\u3057\u3001\u30e1\u30bf\u30c7\u30fc\u30bf\u3092 PostgreSQL \u306b\u4fdd\u5b58\u3057\u307e\u3059\u3002ZIP \u306f\u958b\u767a\u74b0\u5883\u3067\u306f\u30ed\u30fc\u30ab\u30eb\u3001\u672c\u756a ECS \u3067\u306f S3 \u306b\u4fdd\u7ba1\u3067\u304d\u307e\u3059\u3002",
  caution: "\u904b\u7528\u4e0a\u306e\u6ce8\u610f",
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
  "Next.js - \u4e00\u89a7\u30fb\u691c\u7d22\u30fb\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u30fb\u8a73\u7d30\u30fbGit \u9023\u643a",
  "FastAPI - Skill CRUD\u30fbZIP \u89e3\u6790\u30fbGit \u540c\u671f",
  "PostgreSQL - Skill\u30fb\u30bf\u30b0\u30fbGit \u30bd\u30fc\u30b9\u60c5\u5831",
  "Docker / ECS - \u958b\u767a\u74b0\u5883\u3068 AWS \u672c\u756a\u5b9f\u884c\u74b0\u5883",
];

const steps = [
  {
    number: "01",
    title: "\u30ab\u30bf\u30ed\u30b0\u3092\u691c\u7d22\u3059\u308b",
    description:
      "\u30c8\u30c3\u30d7\u753b\u9762\u306e\u691c\u7d22\u6b04\u306b\u540d\u524d\u30fb\u8aac\u660e\u30fb\u30bf\u30b0\u3092\u5165\u529b\u3057\u307e\u3059\u3002\u30ab\u30c6\u30b4\u30ea\u3068\u767b\u9332\u5143\uff08Upload / Git\uff09\u3092\u7d44\u307f\u5408\u308f\u305b\u3066\u7d5e\u308a\u8fbc\u3081\u307e\u3059\u3002",
    note:
      "\u30ab\u30fc\u30c9\u3092\u9078\u629e\u3059\u308b\u3068\u3001SKILL.md \u306e\u5185\u5bb9\u30fb\u4f5c\u8005\u30fb\u30d0\u30fc\u30b8\u30e7\u30f3\u30fb\u30bf\u30b0\u30fb\u66f4\u65b0\u65e5\u6642\u3092\u78ba\u8a8d\u3067\u304d\u307e\u3059\u3002",
  },
  {
    number: "02",
    title: "ZIP \u304b\u3089 Skill \u3092\u767b\u9332\u3059\u308b",
    description:
      "Upload \u3092\u958b\u304d\u3001SKILL.md \u3092\u542b\u3080 ZIP \u30d5\u30a1\u30a4\u30eb\u3092\u30c9\u30e9\u30c3\u30b0\uff06\u30c9\u30ed\u30c3\u30d7\u3057\u307e\u3059\u3002YAML frontmatter \u306e\u60c5\u5831\u306f\u81ea\u52d5\u3067\u8aad\u307f\u53d6\u3089\u308c\u307e\u3059\u3002",
    note:
      "\u540d\u524d\u30fb\u8aac\u660e\u30fb\u30ab\u30c6\u30b4\u30ea\u30fb\u4f5c\u8005\u30fb\u30d0\u30fc\u30b8\u30e7\u30f3\u30fb\u30bf\u30b0\u306f\u767b\u9332\u6642\u306b\u4e0a\u66f8\u304d\u3067\u304d\u307e\u3059\u3002\u30d5\u30a1\u30a4\u30eb\u4e0a\u9650\u306f 50MB \u3067\u3059\u3002",
  },
  {
    number: "03",
    title: "Git \u30ea\u30dd\u30b8\u30c8\u30ea\u3092\u9023\u643a\u3059\u308b",
    description:
      "Git Sync \u3067\u8868\u793a\u540d\u3001\u30ea\u30dd\u30b8\u30c8\u30ea URL\u3001\u30d6\u30e9\u30f3\u30c1\u3092\u767b\u9332\u3057\u307e\u3059\u3002\u5fc5\u8981\u306b\u5fdc\u3058\u3066 Skills \u306e\u30b5\u30d6\u30c7\u30a3\u30ec\u30af\u30c8\u30ea\u3068\u30a2\u30af\u30bb\u30b9\u30c8\u30fc\u30af\u30f3\u3092\u6307\u5b9a\u3057\u307e\u3059\u3002",
    note:
      "Sync \u3092\u5b9f\u884c\u3059\u308b\u3068 SKILL.md \u3092\u518d\u5e30\u691c\u7d22\u3057\u3001\u65b0\u898f\u767b\u9332\u30fb\u65e2\u5b58 Skill \u306e\u66f4\u65b0\u30fb\u524a\u9664\u72b6\u614b\u306e\u53cd\u6620\u3092\u884c\u3044\u307e\u3059\u3002",
  },
  {
    number: "04",
    title: "\u5185\u5bb9\u3092\u78ba\u8a8d\u30fb\u5171\u6709\u3059\u308b",
    description:
      "\u8a73\u7d30\u753b\u9762\u3067\u624b\u9806\u672c\u6587\u3068\u30e1\u30bf\u30c7\u30fc\u30bf\u3092\u78ba\u8a8d\u3057\u307e\u3059\u3002\u5171\u6709\u6642\u306f\u30d6\u30e9\u30a6\u30b6\u306e\u8a73\u7d30\u753b\u9762 URL \u3092\u793e\u5185\u30e1\u30f3\u30d0\u30fc\u3078\u6848\u5185\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
    note:
      "\u4e0d\u8981\u306b\u306a\u3063\u305f Skill \u306f\u8a73\u7d30\u753b\u9762\u304b\u3089\u524a\u9664\u3067\u304d\u307e\u3059\u3002Git \u7531\u6765\u306e Skill \u306f\u6b21\u56de\u540c\u671f\u3067\u3082\u72b6\u614b\u304c\u66f4\u65b0\u3055\u308c\u307e\u3059\u3002",
  },
];

const cautions = [
  "\u6a5f\u5bc6\u60c5\u5831\u3084\u8a8d\u8a3c\u60c5\u5831\u3092 SKILL.md \u3084 ZIP \u306b\u542b\u3081\u306a\u3044\u3067\u304f\u3060\u3055\u3044\u3002",
  "\u30d7\u30e9\u30a4\u30d9\u30fc\u30c8 Git \u306e\u30c8\u30fc\u30af\u30f3\u306f\u5fc5\u8981\u6700\u5c0f\u9650\u306e\u6a29\u9650\u306b\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
  "\u5171\u6709\u524d\u306b\u4f5c\u8005\u30fb\u30d0\u30fc\u30b8\u30e7\u30f3\u30fb\u624b\u9806\u5185\u5bb9\u3092\u78ba\u8a8d\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
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
