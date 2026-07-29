"""Append a clean CI/CD section to the ECS README (ASCII-safe source)."""

from pathlib import Path

path = Path(__file__).resolve().parents[1] / "infrastructure" / "ecs" / "README.md"
text = path.read_text(encoding="utf-8")

# Drop any previously appended broken section.
marker = "\n## CI/CD (GitHub Actions)"
if marker in text:
    text = text.split(marker, 1)[0].rstrip() + "\n"

extra = r'''
## CI/CD (GitHub Actions)

Workflows live in `.github/workflows/`:

- `ci.yml` - always runs on PR / push to `main`
- `deploy-ecs.yml` - deploys to ECS on manual run, or on push when `ENABLE_ECS_DEPLOY=true`

### One-time AWS setup

1. Create ECR repositories: `skills-catalog-backend`, `skills-catalog-frontend`
2. Create ECS cluster/service `skills-catalog` with the Fargate task definition
3. Create CloudWatch log group `/ecs/skills-catalog`
4. Store `DATABASE_URL` in Secrets Manager (`skills-catalog/database-url`)
5. Create an IAM role for GitHub Actions (OIDC recommended) with:
   - ECR push/pull
   - `ecs:RegisterTaskDefinition`, `ecs:UpdateService`, `ecs:DescribeServices`
   - `iam:PassRole` for the task execution / task roles

### GitHub configuration

Repository **Variables**

| Name | Example |
|---|---|
| `ENABLE_ECS_DEPLOY` | `true` |
| `AWS_REGION` | `ap-northeast-1` |
| `ECS_CLUSTER` | `skills-catalog` |
| `ECS_SERVICE` | `skills-catalog` |
| `ECR_BACKEND_REPO` | `skills-catalog-backend` |
| `ECR_FRONTEND_REPO` | `skills-catalog-frontend` |
| `FRONTEND_API_BASE_URL` | `https://api.skills.example.com/api/v1` |

Repository / Environment **Secrets** (`production` environment)

| Name | Description |
|---|---|
| `AWS_ROLE_TO_ASSUME` | Preferred. IAM role ARN trusted by GitHub OIDC |
| `AWS_ACCESS_KEY_ID` | Fallback if OIDC is not used |
| `AWS_SECRET_ACCESS_KEY` | Fallback if OIDC is not used |

### First deploy

1. Open Actions -> **Deploy ECS** -> **Run workflow**
2. Confirm the service becomes stable in the ECS console
3. Optionally set `ENABLE_ECS_DEPLOY=true` for automatic deploys on `main`
'''

path.write_text(text.rstrip() + "\n" + extra, encoding="utf-8", newline="\n")
print("rewrote ECS README CI/CD section")
