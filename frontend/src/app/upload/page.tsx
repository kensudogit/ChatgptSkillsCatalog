"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useCallback, useState, type DragEvent } from "react";
import { api } from "@/lib/api";

export default function UploadPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("");
  const [author, setAuthor] = useState("");
  const [version, setVersion] = useState("");
  const [tags, setTags] = useState("");
  const [drag, setDrag] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((e: DragEvent) => {
    e.preventDefault();
    setDrag(false);
    const f = e.dataTransfer.files?.[0];
    if (f) setFile(f);
  }, []);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!file) {
      setError("Please select a ZIP file");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const form = new FormData();
      form.append("file", file);
      if (name) form.append("name", name);
      if (description) form.append("description", description);
      if (category) form.append("category", category);
      if (author) form.append("author", author);
      if (version) form.append("version", version);
      if (tags) form.append("tags", tags);

      const skill = await api.uploadSkill(form);
      router.push(`/skills/${skill.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Upload Skill</h1>
          <p>
            Register a ChatGPT / Cursor Skill ZIP that contains SKILL.md.
            Metadata is extracted from YAML frontmatter when available.
          </p>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <form className="panel form-grid" onSubmit={onSubmit}>
        <div
          className={`dropzone ${drag ? "active" : ""}`}
          onDragOver={(e) => {
            e.preventDefault();
            setDrag(true);
          }}
          onDragLeave={() => setDrag(false)}
          onDrop={onDrop}
          onClick={() => document.getElementById("file-input")?.click()}
        >
          <input
            id="file-input"
            type="file"
            accept=".zip,application/zip"
            hidden
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          />
          {file ? (
            <p>
              Selected: <strong style={{ color: "var(--text)" }}>{file.name}</strong>
              <br />
              <span className="stat-inline">{(file.size / 1024).toFixed(1)} KB</span>
            </p>
          ) : (
            <p>
              Drag and drop a ZIP, or click to choose
              <br />
              <span className="stat-inline">SKILL.md required / max 50MB</span>
            </p>
          )}
        </div>

        <label>
          Name (optional)
          <input
            className="text-input"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="pcb-design-review"
          />
        </label>

        <label>
          Description (optional)
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
            Category
            <input
              className="text-input"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              placeholder="design-review"
            />
          </label>
          <label>
            Author
            <input
              className="text-input"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
            />
          </label>
          <label>
            Version
            <input
              className="text-input"
              value={version}
              onChange={(e) => setVersion(e.target.value)}
              placeholder="1.0.0"
            />
          </label>
        </div>

        <label>
          Tags (comma-separated)
          <input
            className="text-input"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            placeholder="pcb, review, quality"
          />
        </label>

        <div className="form-actions">
          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading ? "Uploading..." : "Register"}
          </button>
          <button
            className="btn btn-ghost"
            type="button"
            onClick={() => router.push("/")}
          >
            Cancel
          </button>
        </div>
      </form>
    </>
  );
}
