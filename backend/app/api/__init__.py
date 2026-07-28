from fastapi import APIRouter

from app.api import git_sources, skills

api_router = APIRouter()
api_router.include_router(skills.router)
api_router.include_router(git_sources.router)
