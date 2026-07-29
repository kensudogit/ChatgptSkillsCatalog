"""Inquiry API: answer questions about the Skills catalog."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.database import get_db
from app.services.inquiry import answer_inquiry

router = APIRouter(prefix="/inquire", tags=["inquire"])


class InquireRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


class InquireSkillRef(BaseModel):
    id: int
    name: str
    description: str
    category: str | None = None
    tags: list[str] = Field(default_factory=list)


class InquireResponse(BaseModel):
    answer: str
    mode: str
    skills: list[InquireSkillRef] = Field(default_factory=list)
    error: str | None = None


class InquireStatus(BaseModel):
    openai_configured: bool
    model: str


@router.get("/status", response_model=InquireStatus)
def inquire_status(settings: Settings = Depends(get_settings)):
    return InquireStatus(
        openai_configured=bool(settings.openai_api_key),
        model=settings.openai_model,
    )


@router.post("", response_model=InquireResponse)
def inquire(
    payload: InquireRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")
    result = answer_inquiry(db, settings, question)
    return InquireResponse(**result)
