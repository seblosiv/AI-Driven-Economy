"""
Quiz response model.
"""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Column, JSON


class QuizResponse(SQLModel, table=True):
    """User's quiz responses and input data."""

    __tablename__ = "quiz_responses"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)

    # Demographics
    country: str = Field(max_length=100)
    age_range: str = Field(max_length=50)  # "18-24", "25-34", etc.

    # Occupation
    occupation_id: Optional[int] = Field(default=None, foreign_key="occupations.id")
    current_job_title: str = Field(max_length=255)
    current_salary: Optional[float] = Field(default=None)

    # Skills & interests (stored as JSON arrays)
    skills: dict = Field(default={}, sa_column=Column(JSON))
    creative_interests: dict = Field(default={}, sa_column=Column(JSON))

    # Planning inputs
    risk_tolerance: str = Field(max_length=50)  # "low", "medium", "high"
    time_horizon: int = Field(default=5, description="Planning horizon in years")
    learning_hours_per_week: float = Field(
        default=0.0,
        description="Hours available for learning weekly"
    )

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
