# ChatGPT Skills Catalog

Internal web application for centrally managing, searching, and sharing ChatGPT Skills.

## Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15 / React 19 / TypeScript |
| Backend | FastAPI / SQLAlchemy / Python 3.12 |
| Database | PostgreSQL 16 |
| Runtime | Docker Compose (dev) / AWS ECS Fargate (prod) |

```
ChatgptSkillsCatalog/
|- frontend/            # Next.js UI
|- backend/             # FastAPI API
|- infrastructure/ecs/  # ECS task definition & deploy notes
|- Dockerfile           # Combined image for Railway (single URL)
|- railway.toml         # Railway build & health-check settings
|- start.sh             # Runs uvicorn + Next.js in one container
|- docker-compose.yml
\- samples/             # Sample Skill package
```

## Features

- **ZIP upload**: Register Skill ZIPs that contain `SKILL.md` (metadata from YAML frontmatter)
- **List & search**: Filter by name / description / tags / category / source (`upload` | `git`)
- **Detail view**: Inspect SKILL.md body and metadata; delete skills
- **Git sync**: Register a repository, clone/pull, recursively scan `SKILL.md`, import into catalog
- **Storage**: Local volume in development; S3-ready for ECS (`STORAGE_BACKEND=s3`)

## Quick start (Docker)

If Docker Desktop bake fails with a buildx context error, disable bake first:

```powershell
$env:COMPOSE_BAKE="false"
docker compose up --build
```

Or build images directly, then start without rebuild:

```powershell
docker build -t chatgptskillscatalog-backend ./backend
docker build -t chatgptskillscatalog-frontend -f ./frontend/Dockerfile.dev ./frontend
$env:COMPOSE_BAKE="false"
docker compose up -d --no-build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend Swagger | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 (`skills` / `skills`) |

Stop:

```bash
docker compose down
```

## Local development (without full stack Docker)

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

set DATABASE_URL=postgresql+psycopg2://skills:skills@localhost:5432/skills_catalog
set UPLOAD_DIR=%CD%\uploads
set GIT_WORKDIR=%CD%\git_repos
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API overview

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/skills` | List/search (`q`, `category`, `source_type`, `tag`, `page`) |
| POST | `/api/v1/skills/upload` | ZIP upload (multipart) |
| GET | `/api/v1/skills/{id}` | Detail |
| PATCH | `/api/v1/skills/{id}` | Update metadata |
| DELETE | `/api/v1/skills/{id}` | Delete |
| GET/POST | `/api/v1/git-sources` | List / register Git sources |
| POST | `/api/v1/git-sources/{id}/sync` | Sync repository |
| GET | `/health` | Health check |

## Skill ZIP format

```
my-skill/
|- SKILL.md      # required (YAML frontmatter recommended)
\- ...           # optional supporting files
```

Example `SKILL.md`:

```markdown
---
name: pcb-design-review
description: Assist PCB design reviews
version: 1.0.0
author: design-team
category: design-review
tags: [pcb, review]
---

# PCB Design Review

Guide reviewers through design checkpoints...
```

Sample package: `samples/sample-skill/`
Prebuilt ZIP: `samples/sample-pcb-checklist.zip`

```bash
python scripts/make_sample_zip.py
```

## Railway deployment

Railway builds the repository root, so the root `Dockerfile` packages the Next.js
frontend and the FastAPI backend into a single container served on one URL.
Next.js listens on `$PORT` and proxies `/api/*`, `/health`, `/docs` and
`/openapi.json` to the internal uvicorn process on `127.0.0.1:8000`.

1. Add a PostgreSQL database to the Railway project
2. Set the service variables:

| Variable | Value |
|---|---|
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` (reference variable) |
| `STORAGE_BACKEND` | `local`, or `s3` with `S3_BUCKET` + AWS credentials |

3. Deploy. `railway.toml` selects the Dockerfile builder and health-checks `/health`.

Notes:

- The container filesystem is ephemeral. Attach a Railway volume for
  `/app/uploads` and `/app/git_repos`, or use `STORAGE_BACKEND=s3`, to keep
  uploaded ZIPs across deploys.
- `NEXT_PUBLIC_API_BASE_URL` is fixed to `/api/v1` at image build time, so no
  public API URL is required.
- Driver-less URLs (`postgres://`, `postgresql://`) are normalized to
  `postgresql+psycopg2://` by the backend settings.

## AWS ECS deployment

See [infrastructure/ecs/README.md](infrastructure/ecs/README.md).

Summary:

1. Push backend / frontend images to ECR
2. Prepare RDS PostgreSQL, S3 bucket, Secrets Manager
3. Register `task-definition.json` and update the ECS service

## Backend environment variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | compose DB URL | SQLAlchemy URL |
| `UPLOAD_DIR` | `/app/uploads` | Local upload directory |
| `STORAGE_BACKEND` | `local` | `local` or `s3` |
| `S3_BUCKET` | - | Required when using S3 |
| `CORS_ORIGINS` | `http://localhost:3000` | Comma-separated origins |
| `GIT_WORKDIR` | `/app/git_repos` | Clone working directory |

## Frontend environment variables

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_BASE_URL` | API base URL (e.g. `http://localhost:8000/api/v1`) |

> Production builds embed `NEXT_PUBLIC_*` at build time. Pass the public API URL via `--build-arg` when building the ECS frontend image.
"# ChatgptSkillsCatalog" 
