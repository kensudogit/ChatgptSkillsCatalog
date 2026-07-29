# Skills Catalog - AWS ECS (Fargate) deploy guide

## Prerequisites

- AWS CLI and Docker available
- ECR repositories:
  - `skills-catalog-backend`
  - `skills-catalog-frontend`
- RDS PostgreSQL (or Aurora)
- S3 bucket for ZIP uploads
- ALB + target groups (ports 3000 / 8000)
- `DATABASE_URL` stored in Secrets Manager

## 1. Build and push images

```bash
export AWS_REGION=ap-northeast-1
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export IMAGE_TAG=$(git rev-parse --short HEAD)

aws ecr get-login-password --region $AWS_REGION \
  | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Backend
docker build -t skills-catalog-backend:$IMAGE_TAG ./backend
docker tag skills-catalog-backend:$IMAGE_TAG \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/skills-catalog-backend:$IMAGE_TAG
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/skills-catalog-backend:$IMAGE_TAG

# Frontend (embed public API URL at build time)
docker build \
  --build-arg NEXT_PUBLIC_API_BASE_URL=https://api.skills.example.com/api/v1 \
  -t skills-catalog-frontend:$IMAGE_TAG \
  -f ./frontend/Dockerfile \
  ./frontend
docker tag skills-catalog-frontend:$IMAGE_TAG \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/skills-catalog-frontend:$IMAGE_TAG
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/skills-catalog-frontend:$IMAGE_TAG
```

## 2. Register task definition

Replace `ACCOUNT_ID`, secret ARNs, and image tags in `task-definition.json`, then:

```bash
aws ecs register-task-definition --cli-input-json file://infrastructure/ecs/task-definition.json
```

## 3. Update service

```bash
aws ecs update-service \
  --cluster skills-catalog \
  --service skills-catalog \
  --task-definition skills-catalog \
  --force-new-deployment
```

## Recommended architecture

| Component | Role |
|---|---|
| ECS Fargate | Frontend + API containers |
| ALB | HTTPS termination / host or path routing |
| RDS PostgreSQL | Skills and Git source metadata |
| S3 | ZIP binary storage (`STORAGE_BACKEND=s3`) |
| CloudWatch Logs | Container logs |
| Secrets Manager | DB URL / optional Git PAT |

## Minimum task role permissions

- `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject` on the uploads bucket
- Secrets Manager read (execution role is also fine)
- ECR pull (execution role)

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
