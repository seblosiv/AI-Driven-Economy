"""
Personal plan generation endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session
from app.backend.db.session import get_session
from app.backend.services.ai_service import ai_service


router = APIRouter(prefix="/api/plan", tags=["plan"])


class PlanRequest(BaseModel):
    """Plan generation request."""
    occupation: str
    skills: List[str]
    interests: List[str]
    risk_tolerance: str
    learning_hours_per_week: float
    user_id: Optional[int] = None


class TrackModule(BaseModel):
    """Learning module in a track."""
    title: str
    description: str
    affiliate_link: str


class Track(BaseModel):
    """Career transition track."""
    name: str
    timeline: str
    description: str
    modules: List[TrackModule]
    success_factors: List[str]


class PlanResponse(BaseModel):
    """Personal plan response."""
    summary: str
    tracks: List[Track]
    wellbeing_tips: List[str]
    resources: List[dict]


@router.post("/generate", response_model=PlanResponse)
async def generate_plan(
    request: PlanRequest,
    session: Session = Depends(get_session)
):
    """
    Generate personalized career transition plan.

    Uses AI provider (with rules-based fallback) to create
    three transition tracks: Fast, Balanced, and Deep.
    """
    plan = await ai_service.generate_career_plan(
        occupation=request.occupation,
        skills=request.skills,
        interests=request.interests,
        risk_tolerance=request.risk_tolerance,
        learning_hours=request.learning_hours_per_week
    )

    return PlanResponse(
        summary=plan.summary,
        tracks=[
            Track(
                name=track.name,
                timeline=track.timeline,
                description=track.description,
                modules=[
                    TrackModule(**module)
                    for module in track.modules
                ],
                success_factors=track.success_factors
            )
            for track in plan.tracks
        ],
        wellbeing_tips=plan.wellbeing_tips,
        resources=plan.resources
    )
