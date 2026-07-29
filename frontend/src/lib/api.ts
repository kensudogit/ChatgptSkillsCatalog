export type CompatIssue = {
  code: string;
  severity: "error" | "warn" | "info" | string;
  message: string;
};

export type ClaudeCompat = {
  compatible: boolean;
  status: "ok" | "warn" | "error" | string;
  summary: string;
  issues: CompatIssue[];
};

export type SkillSummary = {
  id: number;
  name: string;
  description: string;
  version: string | null;
  author: string | null;
  category: string | null;
  source_type: "upload" | "git" | string;
  original_filename: string | null;
  git_source_id: number | null;
  git_path: string | null;
  git_commit: string | null;
  created_at: string;
  updated_at: string;
  tags: string[];
  downloadable: boolean;
  package_dir: string | null;
  claude_compat: ClaudeCompat;
};

export type Skill = SkillSummary & {
  skill_md_content: string | null;
};

export type SkillListResponse = {
  items: SkillSummary[];
  total: number;
  page: number;
  page_size: number;
};

export type GitSource = {
  id: number;
  name: string;
  repository_url: string;
  branch: string;
  skills_subdir: string;
  has_token: boolean;
  last_synced_at: string | null;
  last_sync_status: string | null;
  last_sync_message: string | null;
  created_at: string;
  updated_at: string;
  skill_count: number;
};

export type SyncSkipItem = {
  path: string;
  reason: string;
};

export type SyncResult = {
  git_source_id: number;
  status: string;
  message: string;
  imported: number;
  updated: number;
  skipped: number;
  skipped_details?: SyncSkipItem[];
};

export type TestCaseResult = {
  nodeid: string;
  outcome: string;
  duration_ms: number;
  longrepr?: string | null;
  keywords?: string[];
};

export type TestClassResult = {
  class_name: string;
  passed: number;
  failed: number;
  skipped: number;
  error: number;
  tests: TestCaseResult[];
};

export type TestRunResult = {
  status: string;
  message: string;
  started_at?: string | null;
  finished_at?: string | null;
  duration_ms: number;
  exitstatus?: number | null;
  summary: {
    total: number;
    passed: number;
    failed: number;
    skipped: number;
    error: number;
  };
  tests: TestCaseResult[];
  by_class: TestClassResult[];
  running: boolean;
};

export type InquireSkillRef = {
  id: number;
  name: string;
  description: string;
  category: string | null;
  tags: string[];
};

export type InquireResponse = {
  answer: string;
  mode: string;
  skills: InquireSkillRef[];
  error?: string | null;
};

export type InquireStatus = {
  openai_configured: boolean;
  model: string;
};

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      ...(init?.body instanceof FormData
        ? {}
        : { "Content-Type": "application/json" }),
      ...init?.headers,
    },
    cache: "no-store",
  });

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || JSON.stringify(body);
    } catch {
      /* ignore */
    }
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }

  if (res.status === 204) {
    return undefined as T;
  }
  return res.json() as Promise<T>;
}

export type SkillQuery = {
  q?: string;
  category?: string;
  source_type?: string;
  tag?: string;
  sort?: string;
  claude_compat?: string;
  page?: number;
  page_size?: number;
};

export const api = {
  listSkills(query: SkillQuery = {}) {
    const params = new URLSearchParams();
    Object.entries(query).forEach(([k, v]) => {
      if (v !== undefined && v !== "") params.set(k, String(v));
    });
    const qs = params.toString();
    return request<SkillListResponse>(`/skills${qs ? `?${qs}` : ""}`);
  },

  getSkill(id: number) {
    return request<Skill>(`/skills/${id}`);
  },

  listCategories() {
    return request<{ categories: string[] }>("/skills/categories");
  },

  listTags() {
    return request<{ tags: string[] }>("/skills/tags");
  },

  async uploadSkill(form: FormData) {
    return request<Skill>("/skills/upload", { method: "POST", body: form });
  },

  updateSkill(
    id: number,
    payload: Partial<{
      name: string;
      description: string;
      version: string;
      author: string;
      category: string;
      tags: string[];
    }>
  ) {
    return request<Skill>(`/skills/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload),
    });
  },

  deleteSkill(id: number) {
    return request<void>(`/skills/${id}`, { method: "DELETE" });
  },

  async downloadSkill(id: number, fallbackName = "skill.zip") {
    const res = await fetch(`${API_BASE}/skills/${id}/download`, {
      cache: "no-store",
    });
    if (!res.ok) {
      let detail = res.statusText;
      try {
        const body = await res.json();
        detail = body.detail || detail;
      } catch {
        /* ignore */
      }
      throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
    }
    const blob = await res.blob();
    const disposition = res.headers.get("Content-Disposition") || "";
    const match = /filename="?([^"]+)"?/i.exec(disposition);
    const filename = match?.[1] || fallbackName;
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  },

  listGitSources() {
    return request<GitSource[]>("/git-sources");
  },

  createGitSource(payload: {
    name: string;
    repository_url: string;
    branch?: string;
    skills_subdir?: string;
    access_token?: string;
  }) {
    return request<GitSource>("/git-sources", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  deleteGitSource(id: number) {
    return request<void>(`/git-sources/${id}`, { method: "DELETE" });
  },

  syncGitSource(id: number) {
    return request<SyncResult>(`/git-sources/${id}/sync`, { method: "POST" });
  },

  getTestStatus() {
    return request<TestRunResult>("/tests/status");
  },

  runTests() {
    return request<TestRunResult>("/tests/run", { method: "POST" });
  },

  getInquireStatus() {
    return request<InquireStatus>("/inquire/status");
  },

  inquire(question: string) {
    return request<InquireResponse>("/inquire", {
      method: "POST",
      body: JSON.stringify({ question }),
    });
  },
};
