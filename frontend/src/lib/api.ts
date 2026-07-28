export type Skill = {
  id: number;
  name: string;
  description: string;
  version: string | null;
  author: string | null;
  category: string | null;
  source_type: "upload" | "git" | string;
  original_filename: string | null;
  skill_md_content: string | null;
  git_source_id: number | null;
  git_path: string | null;
  git_commit: string | null;
  created_at: string;
  updated_at: string;
  tags: string[];
};

export type SkillListResponse = {
  items: Skill[];
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

export type SyncResult = {
  git_source_id: number;
  status: string;
  message: string;
  imported: number;
  updated: number;
  skipped: number;
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
};
