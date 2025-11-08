"""
Automation prediction endpoints.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from app.backend.db.session import get_session
from app.backend.models.occupation import Occupation
from app.backend.models.prediction import AutomationPrediction
from app.backend.services.automation_scorer import scorer


router = APIRouter(prefix="/api/predict", tags=["predictions"])


class AutomationRequest(BaseModel):
    """Automation prediction request."""
    occupation_id: int
    user_id: Optional[int] = None
    quiz_response_id: Optional[int] = None


class AutomationResponse(BaseModel):
    """Automation prediction response."""
    band: str
    eta_years: int
    confidence: float
    automation_score: float
    drivers: dict
    explanation: str


@router.post("/automation", response_model=AutomationResponse)
def predict_automation(
    request: AutomationRequest,
    session: Session = Depends(get_session)
):
    """
    Predict automation risk and timeline for an occupation.

    Uses deterministic scoring algorithm.
    """
    # Get occupation
    occupation = session.get(Occupation, request.occupation_id)
    if not occupation:
        raise HTTPException(status_code=404, detail="Occupation not found")

    # Calculate score
    result = scorer.calculate_score(occupation)

    # Save prediction
    prediction = AutomationPrediction(
        user_id=request.user_id,
        quiz_response_id=request.quiz_response_id,
        occupation_id=occupation.id,
        automation_score=result.score,
        band=result.band,
        eta_years=result.eta_years,
        confidence=result.confidence,
        drivers=result.drivers,
        explanation=result.explanation
    )

    session.add(prediction)
    session.commit()
    session.refresh(prediction)

    return AutomationResponse(
        band=result.band,
        eta_years=result.eta_years,
        confidence=result.confidence,
        automation_score=result.score,
        drivers=result.drivers,
        explanation=result.explanation
    )
