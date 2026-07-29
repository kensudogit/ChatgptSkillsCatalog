"use client";

import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";
import {
  api,
  type InquireResponse,
  type InquireStatus,
} from "@/lib/api";
import { messages } from "@/lib/messages";

const t = messages.inquire;

type ChatItem = {
  role: "user" | "assistant";
  text: string;
  mode?: string;
  skills?: InquireResponse["skills"];
};

export default function InquirePage() {
  const [question, setQuestion] = useState("");
  const [status, setStatus] = useState<InquireStatus | null>(null);
  const [items, setItems] = useState<ChatItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getInquireStatus().then(setStatus).catch(() => setStatus(null));
  }, []);

  async function submit(q: string) {
    const cleaned = q.trim();
    if (!cleaned) {
      setError(t.empty);
      return;
    }
    setError(null);
    setLoading(true);
    setItems((prev) => [...prev, { role: "user", text: cleaned }]);
    setQuestion("");
    try {
      const res = await api.inquire(cleaned);
      setItems((prev) => [
        ...prev,
        {
          role: "assistant",
          text: res.answer,
          mode: res.mode,
          skills: res.skills,
        },
      ]);
    } catch (e) {
      setError(e instanceof Error ? e.message : messages.common.loadFailed);
    } finally {
      setLoading(false);
    }
  }

  function onSubmit(event: FormEvent) {
    event.preventDefault();
    void submit(question);
  }

  return (
    <>
      <div className="page-header">
        <div>
          <h1>{t.title}</h1>
          <p>{t.lead}</p>
        </div>
        <span
          className={`badge ${status?.openai_configured ? "badge-accent" : ""}`}
        >
          {status?.openai_configured
            ? `${t.configured} (${status.model})`
            : t.notConfigured}
        </span>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <section className="inquire-suggestions">
        {t.suggestions.map((s) => (
          <button
            key={s}
            type="button"
            className="btn btn-ghost"
            disabled={loading}
            onClick={() => void submit(s)}
          >
            {s}
          </button>
        ))}
      </section>

      <section className="inquire-chat" aria-live="polite">
        {items.length === 0 && (
          <div className="empty-state">
            <p>{t.placeholder}</p>
          </div>
        )}
        {items.map((item, idx) => (
          <article
            key={`${item.role}-${idx}`}
            className={`inquire-bubble is-${item.role}`}
          >
            <p style={{ whiteSpace: "pre-wrap", margin: 0 }}>{item.text}</p>
            {item.role === "assistant" && item.mode && (
              <span className="badge" style={{ marginTop: "0.75rem" }}>
                {item.mode === "openai"
                  ? t.modeOpenai
                  : item.mode === "empty"
                    ? t.modeEmpty
                    : t.modeFallback}
              </span>
            )}
            {item.skills && item.skills.length > 0 && (
              <div className="inquire-refs">
                <strong>{t.related}</strong>
                <ul>
                  {item.skills.map((skill) => (
                    <li key={skill.id}>
                      <Link href={`/skills/${skill.id}`}>{skill.name}</Link>
                      <span>{skill.description}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </article>
        ))}
      </section>

      <form className="inquire-form" onSubmit={onSubmit}>
        <textarea
          className="search-input"
          rows={3}
          placeholder={t.placeholder}
          value={question}
          disabled={loading}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button className="btn btn-primary" type="submit" disabled={loading}>
          {loading ? t.asking : t.ask}
        </button>
      </form>
    </>
  );
}
