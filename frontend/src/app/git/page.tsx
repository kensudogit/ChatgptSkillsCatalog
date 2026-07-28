"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { api, type GitSource, type SyncResult } from "@/lib/api";
import {
  confirmDeleteMessage,
  messages,
  syncStatusLabel,
  syncSummary,
} from "@/lib/messages";

export default function GitPage() {
  const [sources, setSources] = useState<GitSource[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [syncingId, setSyncingId] = useState<number | null>(null);

  const [name, setName] = useState("");
  const [url, setUrl] = useState("");
  const [branch, setBranch] = useState("main");
  const [subdir, setSubdir] = useState("");
  const [token, setToken] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setSources(await api.listGitSources());
    } catch (e) {
      setError(e instanceof Error ? e.message : messages.common.loadFailed);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  async function onCreate(e: FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    setSuccess(null);
    try {
      await api.createGitSource({
        name,
        repository_url: url,
        branch: branch || "main",
        skills_subdir: subdir,
        access_token: token || undefined,
      });
      setName("");
      setUrl("");
      setBranch("main");
      setSubdir("");
      setToken("");
      setSuccess(messages.git.created);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : messages.git.registerFailed);
    } finally {
      setSubmitting(false);
    }
  }

  async function onSync(id: number) {
    setSyncingId(id);
    setError(null);
    setSuccess(null);
    try {
      const result: SyncResult = await api.syncGitSource(id);
      if (result.status === "success") {
        setSuccess(
          syncSummary(result.imported, result.updated, result.skipped)
        );
      } else {
        setError(result.message || messages.git.syncFailed);
      }
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : messages.git.syncFailed);
    } finally {
      setSyncingId(null);
    }
  }

  async function onDelete(source: GitSource) {
    if (!confirm(confirmDeleteMessage(source.name))) return;
    try {
      await api.deleteGitSource(source.id);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : messages.common.deleteFailed);
    }
  }

  return (
    <>
      <div className="page-header">
        <div>
          <h1>{messages.git.title}</h1>
          <p>{messages.git.lead}</p>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <form className="panel form-grid" onSubmit={onCreate} style={{ marginBottom: "1.5rem" }}>
        <h2 style={{ margin: 0, fontSize: "1.05rem" }}>{messages.git.formTitle}</h2>
        <label>
          {messages.git.labelName}
          <input
            className="text-input"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder={messages.git.placeholderName}
          />
        </label>
        <label>
          {messages.git.labelUrl}
          <input
            className="text-input"
            required
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://github.com/org/skills-repo.git"
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
            {messages.git.labelBranch}
            <input
              className="text-input"
              value={branch}
              onChange={(e) => setBranch(e.target.value)}
            />
          </label>
          <label>
            {messages.git.labelSubdir}
            <input
              className="text-input"
              value={subdir}
              onChange={(e) => setSubdir(e.target.value)}
              placeholder="skills/"
            />
          </label>
        </div>
        <label>
          {messages.git.labelToken}
          <input
            className="text-input"
            type="password"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            autoComplete="off"
          />
        </label>
        <div className="form-actions">
          <button className="btn btn-primary" type="submit" disabled={submitting}>
            {submitting ? messages.common.saving : messages.common.register}
          </button>
        </div>
      </form>

      <div className="panel" style={{ padding: 0, overflow: "auto" }}>
        {loading ? (
          <div className="loading">{messages.common.loading}</div>
        ) : sources.length === 0 ? (
          <div className="empty-state" style={{ border: "none" }}>
            {messages.git.empty}
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>{messages.git.thName}</th>
                <th>{messages.git.thRepo}</th>
                <th>{messages.git.thStatus}</th>
                <th>{messages.git.thSkills}</th>
                <th>{messages.git.thActions}</th>
              </tr>
            </thead>
            <tbody>
              {sources.map((s) => (
                <tr key={s.id}>
                  <td>
                    <strong>{s.name}</strong>
                    <div className="stat-inline">
                      {s.branch}
                      {s.skills_subdir ? ` / ${s.skills_subdir}` : ""}
                      {s.has_token ? ` / ${messages.git.tokenSet}` : ""}
                    </div>
                  </td>
                  <td>
                    <span className="stat-inline" style={{ wordBreak: "break-all" }}>
                      {s.repository_url}
                    </span>
                  </td>
                  <td>
                    <span className="badge badge-accent">
                      {syncStatusLabel(s.last_sync_status)}
                    </span>
                    {s.last_synced_at && (
                      <div className="stat-inline" style={{ marginTop: 4 }}>
                        {new Date(s.last_synced_at).toLocaleString("ja-JP")}
                      </div>
                    )}
                    {s.last_sync_message && (
                      <div
                        className="stat-inline"
                        style={{ marginTop: 4, maxWidth: 220 }}
                        title={s.last_sync_message}
                      >
                        {s.last_sync_message.slice(0, 80)}
                        {s.last_sync_message.length > 80 ? "..." : ""}
                      </div>
                    )}
                  </td>
                  <td className="stat-inline">{s.skill_count}</td>
                  <td>
                    <div style={{ display: "flex", gap: "0.4rem", flexWrap: "wrap" }}>
                      <button
                        className="btn btn-primary"
                        onClick={() => onSync(s.id)}
                        disabled={syncingId === s.id}
                      >
                        {syncingId === s.id ? messages.git.syncing : messages.git.sync}
                      </button>
                      <button className="btn btn-danger" onClick={() => onDelete(s)}>
                        {messages.common.delete}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}
