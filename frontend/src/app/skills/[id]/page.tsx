"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { api, type Skill } from "@/lib/api";
import { confirmDeleteMessage, messages, sourceLabel } from "@/lib/messages";

export default function SkillDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = Number(params.id);
  const [skill, setSkill] = useState<Skill | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [viewMode, setViewMode] = useState<"preview" | "raw">("preview");

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("");
  const [author, setAuthor] = useState("");
  const [version, setVersion] = useState("");
  const [tags, setTags] = useState("");

  useEffect(() => {
    if (!Number.isFinite(id)) return;
    api
      .getSkill(id)
      .then((s) => {
        setSkill(s);
        setName(s.name);
        setDescription(s.description || "");
        setCategory(s.category || "");
        setAuthor(s.author || "");
        setVersion(s.version || "");
        setTags(s.tags.join(", "));
      })
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

  async function onDownload() {
    if (!skill) return;
    setDownloading(true);
    setError(null);
    try {
      await api.downloadSkill(skill.id, skill.original_filename || `${skill.name}.zip`);
    } catch (e) {
      setError(e instanceof Error ? e.message : messages.detail.downloadFailed);
    } finally {
      setDownloading(false);
    }
  }

  async function onCopyLink() {
    try {
      await navigator.clipboard.writeText(window.location.href);
      setNotice(messages.detail.copied);
    } catch {
      setError(messages.detail.copyFailed);
    }
  }

  async function onSave(e: FormEvent) {
    e.preventDefault();
    if (!skill) return;
    setSaving(true);
    setError(null);
    try {
      const updated = await api.updateSkill(skill.id, {
        name,
        description,
        category: category || undefined,
        author: author || undefined,
        version: version || undefined,
        tags: tags
          .split(",")
          .map((t) => t.trim())
          .filter(Boolean),
      });
      setSkill(updated);
      setEditing(false);
      setNotice(messages.detail.saved);
    } catch (err) {
      setError(err instanceof Error ? err.message : messages.detail.saveFailed);
    } finally {
      setSaving(false);
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
        <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", justifyContent: "flex-end" }}>
          {skill.downloadable && (
            <button
              className="btn btn-primary"
              onClick={onDownload}
              disabled={downloading}
              type="button"
            >
              {downloading ? messages.detail.downloading : messages.detail.download}
            </button>
          )}
          <button className="btn btn-ghost" onClick={onCopyLink} type="button">
            {messages.detail.copyLink}
          </button>
          <button
            className="btn btn-ghost"
            onClick={() => setEditing((v) => !v)}
            type="button"
          >
            {editing ? messages.common.cancel : messages.detail.edit}
          </button>
          <button className="btn btn-danger" onClick={onDelete} disabled={deleting} type="button">
            {deleting ? messages.common.deleting : messages.common.delete}
          </button>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {notice && <div className="alert alert-success">{notice}</div>}

      {editing && (
        <form className="panel form-grid" onSubmit={onSave} style={{ marginBottom: "1.25rem" }}>
          <label>
            {messages.upload.labelName.replace("????", "")}
            <input className="text-input" required value={name} onChange={(e) => setName(e.target.value)} />
          </label>
          <label>
            {messages.upload.labelDescription.replace("????", "")}
            <textarea
              className="textarea"
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </label>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
              gap: "1rem",
            }}
          >
            <label>
              {messages.upload.labelCategory}
              <input className="text-input" value={category} onChange={(e) => setCategory(e.target.value)} />
            </label>
            <label>
              {messages.upload.labelAuthor}
              <input className="text-input" value={author} onChange={(e) => setAuthor(e.target.value)} />
            </label>
            <label>
              {messages.upload.labelVersion}
              <input className="text-input" value={version} onChange={(e) => setVersion(e.target.value)} />
            </label>
          </div>
          <label>
            {messages.upload.labelTags}
            <input className="text-input" value={tags} onChange={(e) => setTags(e.target.value)} />
          </label>
          <div className="form-actions">
            <button className="btn btn-primary" type="submit" disabled={saving}>
              {saving ? messages.common.saving : messages.detail.save}
            </button>
          </div>
        </form>
      )}

      <div className="detail-layout">
        <div className="panel">
          <div className="detail-panel-header">
            <h2 style={{ margin: 0, fontSize: "1rem" }}>SKILL.md</h2>
            <div className="view-toggle">
              <button
                type="button"
                className={viewMode === "preview" ? "active" : ""}
                onClick={() => setViewMode("preview")}
              >
                {messages.detail.viewRendered}
              </button>
              <button
                type="button"
                className={viewMode === "raw" ? "active" : ""}
                onClick={() => setViewMode("raw")}
              >
                {messages.detail.viewRaw}
              </button>
            </div>
          </div>
          {viewMode === "preview" ? (
            <div className="markdown-body">
              {skill.skill_md_content ? (
                <ReactMarkdown>{skill.skill_md_content}</ReactMarkdown>
              ) : (
                <p>{messages.detail.emptyBody}</p>
              )}
            </div>
          ) : (
            <pre className="markdown-preview">
              {skill.skill_md_content || messages.detail.emptyBody}
            </pre>
          )}
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
                <Link key={t} href={`/?tag=${encodeURIComponent(t)}`} className="badge badge-accent">
                  #{t}
                </Link>
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
