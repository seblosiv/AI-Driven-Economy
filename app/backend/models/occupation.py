"""
Occupation taxonomy model.
"""
from typing import Optional
from sqlmodel import Field, SQLModel


class Occupation(SQLModel, table=True):
    """
    Occupation taxonomy with automation risk factors.
    Based on SOC codes and automation research.
    """

    __tablename__ = "occupations"

    id: Optional[int] = Field(default=None, primary_key=True)
    soc_code: str = Field(unique=True, index=True, max_length=20)
    title: str = Field(index=True, max_length=255)
    sector: str = Field(index=True, max_length=100)

    # Economic factors
    median_salary: float = Field(default=0.0, description="Median annual salary in USD")

    # Automation risk factors (0-1 scale)
    baseline_risk: float = Field(
        ge=0.0, le=1.0,
        description="Base automation probability from research"
    )
    ai_velocity: float = Field(
        ge=0.0, le=1.0,
        description="Rate of AI advancement in this domain"
    )
    remote_feasibility: float = Field(
        ge=0.0, le=1.0,
        description="How easily work can be done remotely/digitally"
    )

    # Protection factors (0-1 scale, higher = more protected)
    creativity_weight: float = Field(
        ge=0.0, le=1.0,
        description="Creative/artistic skill requirement"
    )
    social_weight: float = Field(
        ge=0.0, le=1.0,
        description="Social/interpersonal skill requirement"
    )
    physical_weight: float = Field(
        ge=0.0, le=1.0,
        default=0.0,
        description="Physical presence/manipulation requirement"
    )

    # Metadata
    description: Optional[str] = Field(default=None, max_length=1000)

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "soc_code": "15-1252",
                "title": "Software Developer",
                "sector": "Technology",
                "median_salary": 110000,
                "baseline_risk": 0.35,
                "ai_velocity": 0.85,
                "remote_feasibility": 0.95,
                "creativity_weight": 0.70,
                "social_weight": 0.40
            }
        }
