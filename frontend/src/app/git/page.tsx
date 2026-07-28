"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { api, type GitSource, type SyncResult } from "@/lib/api";

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
      setError(e instanceof Error ? e.message : "Failed to load");
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
      setSuccess("Git source registered. Run sync to import skills.");
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
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
          `Sync complete: imported ${result.imported} / updated ${result.updated} / skipped ${result.skipped}`
        );
      } else {
        setError(result.message || "Sync failed");
      }
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Sync failed");
    } finally {
      setSyncingId(null);
    }
  }

  async function onDelete(source: GitSource) {
    if (!confirm(`Delete "${source.name}"?`)) return;
    try {
      await api.deleteGitSource(source.id);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Delete failed");
    }
  }

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Git Repository Sync</h1>
          <p>
            Register a Git repository that stores Skills, then scan for SKILL.md
            and import them into the catalog.
          </p>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <form className="panel form-grid" onSubmit={onCreate} style={{ marginBottom: "1.5rem" }}>
        <h2 style={{ margin: 0, fontSize: "1.05rem" }}>Register source</h2>
        <label>
          Display name
          <input
            className="text-input"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Design team skills"
          />
        </label>
        <label>
          Repository URL
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
            Branch
            <input
              className="text-input"
              value={branch}
              onChange={(e) => setBranch(e.target.value)}
            />
          </label>
          <label>
            Skills subdirectory (optional)
            <input
              className="text-input"
              value={subdir}
              onChange={(e) => setSubdir(e.target.value)}
              placeholder="skills/"
            />
          </label>
        </div>
        <label>
          Access token (optional, for private repos)
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
            {submitting ? "Saving..." : "Register"}
          </button>
        </div>
      </form>

      <div className="panel" style={{ padding: 0, overflow: "auto" }}>
        {loading ? (
          <div className="loading">Loading...</div>
        ) : sources.length === 0 ? (
          <div className="empty-state" style={{ border: "none" }}>
            No Git sources registered yet.
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Repository</th>
                <th>Status</th>
                <th>Skills</th>
                <th>Actions</th>
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
                      {s.has_token ? " / token" : ""}
                    </div>
                  </td>
                  <td>
                    <span className="stat-inline" style={{ wordBreak: "break-all" }}>
                      {s.repository_url}
                    </span>
                  </td>
                  <td>
                    <span className="badge badge-accent">
                      {s.last_sync_status || "never"}
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
                        {syncingId === s.id ? "Syncing..." : "Sync"}
                      </button>
                      <button className="btn btn-danger" onClick={() => onDelete(s)}>
                        Delete
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
