"use client";

import type { ClaudeCompat } from "@/lib/api";
import { messages } from "@/lib/messages";

export function ClaudeCompatBadge({
  compat,
  compact = false,
}: {
  compat: ClaudeCompat;
  compact?: boolean;
}) {
  const status = compat.status;
  const label =
    status === "ok"
      ? messages.claudeCompat.ok
      : status === "warn"
        ? messages.claudeCompat.warn
        : messages.claudeCompat.error;
  const className =
    status === "ok"
      ? "badge badge-compat-ok"
      : status === "warn"
        ? "badge badge-compat-warn"
        : "badge badge-compat-error";

  return (
    <span className={className} title={compat.summary}>
      {messages.claudeCompat.label}
      {!compact && <>: {label}</>}
    </span>
  );
}

export function ClaudeCompatPanel({ compat }: { compat: ClaudeCompat }) {
  return (
    <section className="compat-panel">
      <div className="compat-panel-header">
        <h2>{messages.claudeCompat.title}</h2>
        <ClaudeCompatBadge compat={compat} />
      </div>
      <p className="compat-lead">{messages.claudeCompat.lead}</p>
      <p className="compat-summary">{compat.summary}</p>
      {compat.issues.length === 0 ? (
        <p className="stat-inline">{messages.claudeCompat.noIssues}</p>
      ) : (
        <ul className="compat-issues">
          {compat.issues.map((issue) => (
            <li key={`${issue.code}-${issue.message}`} data-severity={issue.severity}>
              <span className="compat-severity">{issue.severity}</span>
              <span>{issue.message}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
