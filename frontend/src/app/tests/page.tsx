"use client";

import { useCallback, useEffect, useState } from "react";
import { api, type TestRunResult } from "@/lib/api";
import { messages } from "@/lib/messages";

const t = messages.tests;

function outcomeClass(outcome: string): string {
  if (outcome === "passed") return "test-outcome is-passed";
  if (outcome === "failed" || outcome === "error") return "test-outcome is-failed";
  if (outcome === "skipped") return "test-outcome is-skipped";
  return "test-outcome";
}

export default function TestsPage() {
  const [result, setResult] = useState<TestRunResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [openClass, setOpenClass] = useState<string | null>(null);

  const loadStatus = useCallback(async () => {
    setError(null);
    try {
      const status = await api.getTestStatus();
      setResult(status);
      setRunning(status.running || status.status === "running");
    } catch (e) {
      setError(e instanceof Error ? e.message : messages.common.loadFailed);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadStatus();
  }, [loadStatus]);

  useEffect(() => {
    if (!running) return;
    const id = setInterval(loadStatus, 2000);
    return () => clearInterval(id);
  }, [running, loadStatus]);

  async function onRun() {
    setRunning(true);
    setError(null);
    try {
      const out = await api.runTests();
      setResult(out);
      setRunning(out.running || out.status === "running");
      if (!out.running && out.status !== "running") {
        await loadStatus();
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : messages.common.loadFailed);
      setRunning(false);
    }
  }

  const summary = result?.summary;

  return (
    <>
      <div className="page-header">
        <div>
          <h1>{t.title}</h1>
          <p>{t.lead}</p>
        </div>
        <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
          <button
            className="btn btn-primary"
            type="button"
            disabled={running}
            onClick={onRun}
          >
            {running ? t.running : t.run}
          </button>
          <button className="btn btn-ghost" type="button" onClick={loadStatus}>
            {t.refresh}
          </button>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {loading && !result ? (
        <div className="loading">{messages.common.loading}</div>
      ) : (
        <>
          <section className="test-summary-panel">
            <div className="test-status-row">
              <span className={`badge test-status-badge is-${result?.status || "idle"}`}>
                {result?.status || t.idle}
              </span>
              <p>{result?.message || t.noResults}</p>
            </div>
            {summary && summary.total > 0 && (
              <div className="test-stat-grid">
                <div>
                  <strong>{summary.total}</strong>
                  <span>{t.summaryTotal}</span>
                </div>
                <div className="is-passed">
                  <strong>{summary.passed}</strong>
                  <span>{t.summaryPassed}</span>
                </div>
                <div className="is-failed">
                  <strong>{summary.failed}</strong>
                  <span>{t.summaryFailed}</span>
                </div>
                <div className="is-skipped">
                  <strong>{summary.skipped}</strong>
                  <span>{t.summarySkipped}</span>
                </div>
                <div className="is-failed">
                  <strong>{summary.error}</strong>
                  <span>{t.summaryError}</span>
                </div>
                <div>
                  <strong>{Math.round(result?.duration_ms || 0)} ms</strong>
                  <span>{t.duration}</span>
                </div>
              </div>
            )}
          </section>

          <section className="test-class-list" aria-label={t.byClass}>
            <h2>{t.byClass}</h2>
            {!result?.by_class?.length ? (
              <div className="empty-state">
                <p>{t.noResults}</p>
              </div>
            ) : (
              result.by_class.map((cls) => {
                const open = openClass === cls.class_name;
                const failed = cls.failed + cls.error;
                return (
                  <article className="test-class-card" key={cls.class_name}>
                    <button
                      type="button"
                      className="test-class-header"
                      onClick={() =>
                        setOpenClass(open ? null : cls.class_name)
                      }
                    >
                      <div>
                        <strong>{cls.class_name}</strong>
                        <span className="stat-inline">
                          {cls.passed} passed / {failed} failed / {cls.skipped}{" "}
                          skipped
                        </span>
                      </div>
                      <span className={outcomeClass(failed ? "failed" : "passed")}>
                        {failed ? "FAIL" : "PASS"}
                      </span>
                    </button>
                    {open && (
                      <ul className="test-case-list">
                        {cls.tests.map((caseResult) => (
                          <li key={caseResult.nodeid}>
                            <div className="test-case-row">
                              <span className={outcomeClass(caseResult.outcome)}>
                                {caseResult.outcome}
                              </span>
                              <code>{caseResult.nodeid.split("::").pop()}</code>
                              <span className="stat-inline">
                                {caseResult.duration_ms} ms
                              </span>
                            </div>
                            {caseResult.longrepr && (
                              <pre className="test-longrepr">{caseResult.longrepr}</pre>
                            )}
                          </li>
                        ))}
                      </ul>
                    )}
                  </article>
                );
              })
            )}
          </section>
        </>
      )}
    </>
  );
}
