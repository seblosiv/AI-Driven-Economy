"""
Automation prediction result model.
"""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Column, JSON


class AutomationPrediction(SQLModel, table=True):
    """Cached automation predictions for occupations."""

    __tablename__ = "automation_predictions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    quiz_response_id: Optional[int] = Field(
        default=None,
        foreign_key="quiz_responses.id"
    )
    occupation_id: int = Field(foreign_key="occupations.id", index=True)

    # Prediction results
    automation_score: float = Field(
        ge=0.0, le=1.0,
        description="Overall automation probability"
    )
    band: str = Field(max_length=50, description="Risk band: Low/Medium/High")
    eta_years: int = Field(description="Years until substantial automation")
    confidence: float = Field(ge=0.0, le=1.0, description="Prediction confidence")

    # Explanation
    drivers: dict = Field(default={}, sa_column=Column(JSON), description="Key risk drivers")
    explanation: Optional[str] = Field(default=None, max_length=2000)

    # AIDE Dividend projections (stored for quick retrieval)
    dividend_y5: Optional[float] = Field(default=None)
    dividend_y10: Optional[float] = Field(default=None)
    dividend_y20: Optional[float] = Field(default=None)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
