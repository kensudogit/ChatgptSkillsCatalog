from fastapi import APIRouter

from app.api import git_sources, inquire, skills, tests

api_router = APIRouter()
api_router.include_router(skills.router)
api_router.include_router(git_sources.router)
api_router.include_router(tests.router)
api_router.include_router(inquire.router)
