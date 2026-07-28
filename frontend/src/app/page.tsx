"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense, useCallback, useEffect, useMemo, useState } from "react";
import { api, type SkillListResponse, type SkillSummary } from "@/lib/api";
import { messages, pageRangeLabel, sourceLabel } from "@/lib/messages";

export default function HomePage() {
  return (
    <Suspense fallback={<div className="loading">{messages.common.loading}</div>}>
      <HomePageInner />
    </Suspense>
  );
}

function HomePageInner() {
  const searchParams = useSearchParams();
  const [data, setData] = useState<SkillListResponse | null>(null);
  const [q, setQ] = useState("");
  const [category, setCategory] = useState("");
  const [sourceType, setSourceType] = useState("");
  const [tag, setTag] = useState(searchParams.get("tag") || "");
  const [sort, setSort] = useState("updated_desc");
  const [categories, setCategories] = useState<string[]>([]);
  const [tags, setTags] = useState<string[]>([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fromUrl = searchParams.get("tag") || "";
    if (fromUrl !== tag) {
      setTag(fromUrl);
      setPage(1);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams]);

  const hasFilters = Boolean(q || category || sourceType || tag);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.listSkills({
        q: q || undefined,
        category: category || undefined,
        source_type: sourceType || undefined,
        tag: tag || undefined,
        sort,
        page,
        page_size: 12,
      });
      setData(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : messages.common.loadFailed);
    } finally {
      setLoading(false);
    }
  }, [q, category, sourceType, tag, sort, page]);

  useEffect(() => {
    api.listCategories().then((r) => setCategories(r.categories)).catch(() => {});
    api.listTags().then((r) => setTags(r.tags)).catch(() => {});
  }, []);

  useEffect(() => {
    const t = setTimeout(load, 200);
    return () => clearTimeout(t);
  }, [load]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "/" && !(e.target instanceof HTMLInputElement) && !(e.target instanceof HTMLTextAreaElement)) {
        e.preventDefault();
        document.getElementById("catalog-search")?.focus();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const emptyMessage = useMemo(() => {
    if (!data || data.items.length > 0) return null;
    return hasFilters ? messages.catalog.emptyFiltered : messages.catalog.emptyCatalog;
  }, [data, hasFilters]);

  function clearFilters() {
    setQ("");
    setCategory("");
    setSourceType("");
    setTag("");
    setSort("updated_desc");
    setPage(1);
  }

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
          id="catalog-search"
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
          value={tag}
          onChange={(e) => {
            setPage(1);
            setTag(e.target.value);
          }}
        >
          <option value="">{messages.catalog.allTags}</option>
          {tags.map((t) => (
            <option key={t} value={t}>
              #{t}
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
        <select
          className="select"
          value={sort}
          onChange={(e) => {
            setPage(1);
            setSort(e.target.value);
          }}
        >
          <option value="updated_desc">{messages.catalog.sortUpdated}</option>
          <option value="name_asc">{messages.catalog.sortName}</option>
          <option value="created_desc">{messages.catalog.sortCreated}</option>
        </select>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {loading && !data ? (
        <div className="loading">{messages.common.loading}</div>
      ) : data && data.items.length === 0 ? (
        <div className="empty-state">
          <p>{emptyMessage || messages.catalog.emptyTitle}</p>
          <p style={{ marginTop: "0.75rem", display: "flex", gap: "0.75rem", justifyContent: "center", flexWrap: "wrap" }}>
            {hasFilters ? (
              <button className="btn btn-ghost" type="button" onClick={clearFilters}>
                {messages.catalog.clearFilters}
              </button>
            ) : (
              <Link href="/upload" className="btn btn-primary">
                {messages.catalog.emptyAction}
              </Link>
            )}
          </p>
        </div>
      ) : (
        <>
          <div className={`skill-grid ${loading ? "is-refreshing" : ""}`}>
            {data?.items.map((skill, i) => (
              <SkillCard
                key={skill.id}
                skill={skill}
                index={i}
                onTagClick={(value) => {
                  setPage(1);
                  setTag(value);
                }}
              />
            ))}
          </div>
          {data && data.total > 0 && (
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
                  disabled={page <= 1 || loading}
                  onClick={() => setPage((p) => p - 1)}
                >
                  {messages.catalog.prev}
                </button>
                <button
                  className="btn btn-ghost"
                  disabled={page * data.page_size >= data.total || loading}
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

function SkillCard({
  skill,
  index,
  onTagClick,
}: {
  skill: SkillSummary;
  index: number;
  onTagClick: (tag: string) => void;
}) {
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
          <button
            key={t}
            type="button"
            className="badge badge-clickable"
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              onTagClick(t);
            }}
          >
            #{t}
          </button>
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
