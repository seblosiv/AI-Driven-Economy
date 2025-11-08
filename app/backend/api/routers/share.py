"""
Social sharing and OG image endpoints.
"""
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session
from app.backend.db.session import get_session
from app.backend.services.og_service import og_service


router = APIRouter(prefix="/api/share", tags=["share"])


class OGImageRequest(BaseModel):
    """OG image generation request."""
    user_id: int
    occupation: str
    band: str
    eta_years: int
    dividend_y10: float


class OGImageResponse(BaseModel):
    """OG image response."""
    image_url: str
    share_text: str


@router.post("/og", response_model=OGImageResponse)
def generate_og_image(
    request: OGImageRequest,
    session: Session = Depends(get_session)
):
    """
    Generate Open Graph image for social sharing.

    Creates a branded image with user's results.
    """
    image_url = og_service.generate_result_card(
        user_id=request.user_id,
        occupation=request.occupation,
        band=request.band,
        eta_years=request.eta_years,
        dividend_y10=request.dividend_y10
    )

    share_text = (
        f"I'm a {request.occupation} with {request.band} automation risk "
        f"(~{request.eta_years} years). My potential AIDE dividend in 10 years: "
        f"${request.dividend_y10:,.0f}/year. Get your future plan at lifeafterai.com"
    )

    return OGImageResponse(
        image_url=image_url,
        share_text=share_text
    )
