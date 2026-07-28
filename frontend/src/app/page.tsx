"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { api, type Skill, type SkillListResponse } from "@/lib/api";
import { messages, pageRangeLabel, sourceLabel } from "@/lib/messages";

export default function HomePage() {
  const [data, setData] = useState<SkillListResponse | null>(null);
  const [q, setQ] = useState("");
  const [category, setCategory] = useState("");
  const [sourceType, setSourceType] = useState("");
  const [categories, setCategories] = useState<string[]>([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.listSkills({
        q: q || undefined,
        category: category || undefined,
        source_type: sourceType || undefined,
        page,
        page_size: 12,
      });
      setData(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : messages.common.loadFailed);
    } finally {
      setLoading(false);
    }
  }, [q, category, sourceType, page]);

  useEffect(() => {
    api.listCategories().then((r) => setCategories(r.categories)).catch(() => {});
  }, []);

  useEffect(() => {
    const t = setTimeout(load, 200);
    return () => clearTimeout(t);
  }, [load]);

  return (
    <>
      <div className="page-header">
        <div>
          <h1>{messages.catalog.title}</h1>
          <p>{messages.catalog.lead}</p>
        </div>
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <Link href="/upload" className="btn btn-primary">
            {messages.catalog.uploadZip}
          </Link>
          <Link href="/git" className="btn btn-ghost">
            {messages.catalog.gitSync}
          </Link>
        </div>
      </div>

      <div className="toolbar">
        <input
          className="search-input"
          placeholder={messages.catalog.searchPlaceholder}
          value={q}
          onChange={(e) => {
            setPage(1);
            setQ(e.target.value);
          }}
        />
        <select
          className="select"
          value={category}
          onChange={(e) => {
            setPage(1);
            setCategory(e.target.value);
          }}
        >
          <option value="">{messages.catalog.allCategories}</option>
          {categories.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
        <select
          className="select"
          value={sourceType}
          onChange={(e) => {
            setPage(1);
            setSourceType(e.target.value);
          }}
        >
          <option value="">{messages.catalog.allSources}</option>
          <option value="upload">{messages.common.sourceUpload}</option>
          <option value="git">{messages.common.sourceGit}</option>
        </select>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {loading && !data ? (
        <div className="loading">{messages.common.loading}</div>
      ) : data && data.items.length === 0 ? (
        <div className="empty-state">
          <p>{messages.catalog.emptyTitle}</p>
          <p style={{ marginTop: "0.5rem" }}>
            <Link href="/upload" style={{ color: "var(--accent-hover)" }}>
              {messages.catalog.emptyAction}
            </Link>
          </p>
        </div>
      ) : (
        <>
          <div className="skill-grid">
            {data?.items.map((skill, i) => (
              <SkillCard key={skill.id} skill={skill} index={i} />
            ))}
          </div>
          {data && (
            <div className="pagination">
              <span className="stat-inline">
                {pageRangeLabel(
                  data.total,
                  (page - 1) * data.page_size + 1,
                  Math.min(page * data.page_size, data.total)
                )}
              </span>
              <div style={{ display: "flex", gap: "0.5rem" }}>
                <button
                  className="btn btn-ghost"
                  disabled={page <= 1}
                  onClick={() => setPage((p) => p - 1)}
                >
                  {messages.catalog.prev}
                </button>
                <button
                  className="btn btn-ghost"
                  disabled={page * data.page_size >= data.total}
                  onClick={() => setPage((p) => p + 1)}
                >
                  {messages.catalog.next}
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </>
  );
}

function SkillCard({ skill, index }: { skill: Skill; index: number }) {
  return (
    <Link
      href={`/skills/${skill.id}`}
      className="skill-card"
      style={{ animationDelay: `${Math.min(index, 8) * 40}ms` }}
    >
      <div className="meta-row">
        <span
          className={`badge ${skill.source_type === "git" ? "badge-info" : "badge-accent"}`}
        >
          {sourceLabel(skill.source_type)}
        </span>
        {skill.category && <span className="badge">{skill.category}</span>}
        {skill.version && <span className="badge">v{skill.version}</span>}
      </div>
      <h2>{skill.name}</h2>
      <p className="desc">{skill.description || messages.common.noDescription}</p>
      <div className="meta-row">
        {skill.tags.slice(0, 4).map((t) => (
          <span key={t} className="badge">
            #{t}
          </span>
        ))}
        {skill.author && (
          <span className="stat-inline" style={{ marginLeft: "auto" }}>
            {skill.author}
          </span>
        )}
      </div>
    </Link>
  );
}
