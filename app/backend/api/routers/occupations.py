"""
Occupation search endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlmodel import Session, select, or_
from app.backend.db.session import get_session
from app.backend.models.occupation import Occupation


router = APIRouter(prefix="/api/occupations", tags=["occupations"])


class OccupationResult(BaseModel):
    """Occupation search result."""
    id: int
    soc_code: str
    title: str
    sector: str
    median_salary: float

    class Config:
        from_attributes = True


@router.get("/search", response_model=List[OccupationResult])
def search_occupations(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(10, le=50, description="Max results"),
    session: Session = Depends(get_session)
):
    """
    Search occupations by title or sector.

    Used for autocomplete in quiz.
    """
    query = f"%{q}%"
    statement = (
        select(Occupation)
        .where(
            or_(
                Occupation.title.ilike(query),
                Occupation.sector.ilike(query)
            )
        )
        .limit(limit)
    )

    occupations = session.exec(statement).all()

    return [
        OccupationResult(
            id=occ.id,
            soc_code=occ.soc_code,
            title=occ.title,
            sector=occ.sector,
            median_salary=occ.median_salary
        )
        for occ in occupations
    ]
