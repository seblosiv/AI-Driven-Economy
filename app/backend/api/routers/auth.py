"""
Authentication endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlmodel import Session
from app.backend.db.session import get_session
from app.backend.services.auth_service import auth_service


router = APIRouter(prefix="/api/auth", tags=["auth"])


class MagicLinkRequest(BaseModel):
    """Request magic link."""
    email: EmailStr


class MagicLinkResponse(BaseModel):
    """Magic link response."""
    message: str
    token: str  # In production, this would be sent via email


class VerifyRequest(BaseModel):
    """Verify magic link token."""
    token: str


class TokenResponse(BaseModel):
    """Auth token response."""
    access_token: str
    token_type: str = "bearer"
    user: dict


@router.post("/magic-link", response_model=MagicLinkResponse)
def request_magic_link(request: MagicLinkRequest):
    """
    Request a magic link for passwordless auth.

    In production, this sends an email. For MVP, returns token directly.
    """
    token = auth_service.send_magic_link(request.email)

    return MagicLinkResponse(
        message="Magic link sent! Check your email.",
        token=token  # For dev/testing only
    )


@router.post("/verify", response_model=TokenResponse)
def verify_magic_link(
    request: VerifyRequest,
    session: Session = Depends(get_session)
):
    """Verify magic link and create session."""
    email = auth_service.verify_magic_link(request.token)

    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Get or create user
    user = auth_service.get_or_create_user(session, email)

    # Create access token
    access_token = auth_service.create_access_token(user.id, user.email)

    return TokenResponse(
        access_token=access_token,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_pro": user.is_pro
        }
    )


@router.get("/me")
def get_current_user(
    token: str,
    session: Session = Depends(get_session)
):
    """Get current user info from token."""
    payload = auth_service.verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload["sub"])
    from app.backend.models.user import User
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "is_pro": user.is_pro,
        "created_at": user.created_at
    }
