"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { api, type Skill } from "@/lib/api";
import { confirmDeleteMessage, messages, sourceLabel } from "@/lib/messages";

export default function SkillDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = Number(params.id);
  const [skill, setSkill] = useState<Skill | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (!Number.isFinite(id)) return;
    api
      .getSkill(id)
      .then(setSkill)
      .catch((e) =>
        setError(e instanceof Error ? e.message : messages.common.loadFailed)
      );
  }, [id]);

  async function onDelete() {
    if (!skill || !confirm(confirmDeleteMessage(skill.name))) return;
    setDeleting(true);
    try {
      await api.deleteSkill(skill.id);
      router.push("/");
    } catch (e) {
      setError(e instanceof Error ? e.message : messages.common.deleteFailed);
      setDeleting(false);
    }
  }

  if (error && !skill) {
    return <div className="alert alert-error">{error}</div>;
  }

  if (!skill) {
    return <div className="loading">{messages.common.loading}</div>;
  }

  return (
    <>
      <div className="page-header">
        <div>
          <p style={{ margin: "0 0 0.5rem" }}>
            <Link href="/" style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
              {messages.detail.back}
            </Link>
          </p>
          <h1>{skill.name}</h1>
          <p>{skill.description || messages.common.noDescription}</p>
        </div>
        <button className="btn btn-danger" onClick={onDelete} disabled={deleting}>
          {deleting ? messages.common.deleting : messages.common.delete}
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="detail-layout">
        <div className="panel">
          <h2 style={{ marginTop: 0, fontSize: "1rem" }}>SKILL.md</h2>
          <pre className="markdown-preview">
            {skill.skill_md_content || messages.detail.emptyBody}
          </pre>
        </div>

        <aside className="panel" style={{ alignSelf: "start" }}>
          <h2 style={{ marginTop: 0, fontSize: "0.85rem", color: "var(--text-dim)" }}>
            {messages.detail.metadata}
          </h2>
          <dl style={{ margin: 0, display: "grid", gap: "0.85rem", fontSize: "0.9rem" }}>
            <Meta
              label={messages.detail.labelSource}
              value={sourceLabel(skill.source_type)}
            />
            <Meta label={messages.detail.labelCategory} value={skill.category} />
            <Meta label={messages.detail.labelVersion} value={skill.version} />
            <Meta label={messages.detail.labelAuthor} value={skill.author} />
            <Meta
              label={messages.detail.labelFilename}
              value={skill.original_filename}
            />
            <Meta label={messages.detail.labelGitPath} value={skill.git_path} />
            <Meta
              label={messages.detail.labelCommit}
              value={skill.git_commit ? skill.git_commit.slice(0, 8) : null}
            />
            <Meta
              label={messages.detail.labelUpdated}
              value={new Date(skill.updated_at).toLocaleString("ja-JP")}
            />
          </dl>
          {skill.tags.length > 0 && (
            <div className="meta-row" style={{ marginTop: "1rem" }}>
              {skill.tags.map((t) => (
                <span key={t} className="badge badge-accent">
                  #{t}
                </span>
              ))}
            </div>
          )}
        </aside>
      </div>
    </>
  );
}

function Meta({ label, value }: { label: string; value: string | null | undefined }) {
  if (!value) return null;
  return (
    <div>
      <dt style={{ color: "var(--text-dim)", fontSize: "0.72rem", marginBottom: 2 }}>
        {label}
      </dt>
      <dd style={{ margin: 0, fontFamily: "var(--font-mono)", fontSize: "0.85rem" }}>
        {value}
      </dd>
    </div>
  );
}
