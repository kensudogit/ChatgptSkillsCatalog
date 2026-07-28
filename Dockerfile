# Single-container image for Railway: Next.js frontend + FastAPI backend on one port.
# Next.js listens on $PORT and proxies /api, /health and /docs to the internal uvicorn.
FROM node:22-bookworm-slim AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ .

# Relative base URL keeps browser requests same-origin so the rewrites can proxy them.
ENV NEXT_PUBLIC_API_BASE_URL=/api/v1
ENV NODE_ENV=production
RUN npm run build

# "next start" is unsupported with output: standalone, so assemble the
# self-contained server bundle that start.sh runs with plain node.
RUN cp -r public .next/standalone/public \
    && cp -r .next/static .next/standalone/.next/static

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git gcc libpq-dev curl ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY --from=frontend-builder /app/frontend/.next/standalone /app/frontend

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh && mkdir -p /app/uploads /app/git_repos

ENV PYTHONUNBUFFERED=1 \
    NODE_ENV=production \
    UPLOAD_DIR=/app/uploads \
    GIT_WORKDIR=/app/git_repos \
    INTERNAL_API_URL=http://127.0.0.1:8000

CMD ["/app/start.sh"]
