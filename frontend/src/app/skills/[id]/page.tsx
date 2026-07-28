"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { api, type Skill } from "@/lib/api";

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
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load"));
  }, [id]);

  async function onDelete() {
    if (!skill || !confirm(`Delete "${skill.name}"?`)) return;
    setDeleting(true);
    try {
      await api.deleteSkill(skill.id);
      router.push("/");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Delete failed");
      setDeleting(false);
    }
  }

  if (error && !skill) {
    return <div className="alert alert-error">{error}</div>;
  }

  if (!skill) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <>
      <div className="page-header">
        <div>
          <p style={{ margin: "0 0 0.5rem" }}>
            <Link href="/" style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
              Back to catalog
            </Link>
          </p>
          <h1>{skill.name}</h1>
          <p>{skill.description || "No description"}</p>
        </div>
        <button className="btn btn-danger" onClick={onDelete} disabled={deleting}>
          {deleting ? "Deleting..." : "Delete"}
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="detail-layout">
        <div className="panel">
          <h2 style={{ marginTop: 0, fontSize: "1rem" }}>SKILL.md</h2>
          <pre className="markdown-preview">
            {skill.skill_md_content || "(empty)"}
          </pre>
        </div>

        <aside className="panel" style={{ alignSelf: "start" }}>
          <h2 style={{ marginTop: 0, fontSize: "0.85rem", color: "var(--text-dim)" }}>
            Metadata
          </h2>
          <dl style={{ margin: 0, display: "grid", gap: "0.85rem", fontSize: "0.9rem" }}>
            <Meta label="Source" value={skill.source_type} />
            <Meta label="Category" value={skill.category} />
            <Meta label="Version" value={skill.version} />
            <Meta label="Author" value={skill.author} />
            <Meta label="Filename" value={skill.original_filename} />
            <Meta label="Git path" value={skill.git_path} />
            <Meta
              label="Commit"
              value={skill.git_commit ? skill.git_commit.slice(0, 8) : null}
            />
            <Meta
              label="Updated"
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
