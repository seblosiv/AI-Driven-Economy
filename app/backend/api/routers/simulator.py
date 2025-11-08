"""
AIDE dividend simulator endpoints.
"""
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session
from app.backend.db.session import get_session
from app.backend.services.dividend_simulator import simulator, DividendParams


router = APIRouter(prefix="/api/simulate", tags=["simulator"])


class SimulateRequest(BaseModel):
    """Dividend simulation request."""
    sector: str
    automation_score: float
    base_salary: float
    country: str = "US"
    tax_rate: float = 0.25
    distribution_share: float = 0.60
    growth_rate: float = 0.03
    contribution_hours_weekly: float = 0.0
    user_id: Optional[int] = None


class SimulateResponse(BaseModel):
    """Dividend simulation response."""
    year_5: float
    year_10: float
    year_20: float
    series: list
    percentage_of_current_salary_y5: float
    percentage_of_current_salary_y10: float
    percentage_of_current_salary_y20: float
    explanation: str


@router.post("/dividend", response_model=SimulateResponse)
def simulate_dividend(
    request: SimulateRequest,
    session: Session = Depends(get_session)
):
    """
    Simulate AIDE dividend projections.

    Returns 5/10/20 year projections with time series.
    """
    params = DividendParams(
        sector=request.sector,
        automation_score=request.automation_score,
        base_salary=request.base_salary,
        country=request.country,
        tax_rate=request.tax_rate,
        distribution_share=request.distribution_share,
        growth_rate=request.growth_rate,
        contribution_hours_weekly=request.contribution_hours_weekly
    )

    result = simulator.simulate(params)

    return SimulateResponse(
        year_5=result.year_5,
        year_10=result.year_10,
        year_20=result.year_20,
        series=result.series,
        percentage_of_current_salary_y5=result.percentage_of_current_salary_y5,
        percentage_of_current_salary_y10=result.percentage_of_current_salary_y10,
        percentage_of_current_salary_y20=result.percentage_of_current_salary_y20,
        explanation=result.explanation
    )
