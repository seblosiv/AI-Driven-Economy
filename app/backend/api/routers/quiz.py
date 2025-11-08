"""
Quiz submission endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from app.backend.db.session import get_session
from app.backend.models.quiz import QuizResponse
from app.backend.models.occupation import Occupation


router = APIRouter(prefix="/api/quiz", tags=["quiz"])


class QuizSubmission(BaseModel):
    """Quiz submission data."""
    country: str
    age_range: str
    current_job_title: str
    current_salary: Optional[float] = None
    skills: List[str]
    creative_interests: List[str]
    risk_tolerance: str  # low, medium, high
    time_horizon: int = 5
    learning_hours_per_week: float = 0.0
    user_id: Optional[int] = None


class QuizSubmissionResponse(BaseModel):
    """Quiz submission response."""
    quiz_id: int
    message: str


@router.post("/submit", response_model=QuizSubmissionResponse)
def submit_quiz(
    submission: QuizSubmission,
    session: Session = Depends(get_session)
):
    """
    Submit quiz responses.

    Creates a quiz response record and returns ID for prediction.
    """
    # Try to find matching occupation
    statement = select(Occupation).where(
        Occupation.title.ilike(f"%{submission.current_job_title}%")
    )
    occupation = session.exec(statement).first()

    # Create quiz response
    quiz_response = QuizResponse(
        user_id=submission.user_id,
        country=submission.country,
        age_range=submission.age_range,
        occupation_id=occupation.id if occupation else None,
        current_job_title=submission.current_job_title,
        current_salary=submission.current_salary,
        skills={"items": submission.skills},
        creative_interests={"items": submission.creative_interests},
        risk_tolerance=submission.risk_tolerance,
        time_horizon=submission.time_horizon,
        learning_hours_per_week=submission.learning_hours_per_week
    )

    session.add(quiz_response)
    session.commit()
    session.refresh(quiz_response)

    return QuizSubmissionResponse(
        quiz_id=quiz_response.id,
        message="Quiz submitted successfully"
    )
