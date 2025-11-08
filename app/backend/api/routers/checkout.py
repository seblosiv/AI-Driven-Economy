"""
Stripe checkout endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlmodel import Session
from app.backend.db.session import get_session
from app.backend.services.stripe_service import stripe_service
from app.backend.services.auth_service import auth_service


router = APIRouter(prefix="/api/checkout", tags=["checkout"])


class CheckoutRequest(BaseModel):
    """Checkout session request."""
    plan_type: str = "monthly"  # monthly or yearly
    token: str  # Auth token


class CheckoutResponse(BaseModel):
    """Checkout session response."""
    session_id: str
    url: str


@router.post("/session", response_model=CheckoutResponse)
def create_checkout_session(
    request: CheckoutRequest,
    session: Session = Depends(get_session)
):
    """
    Create Stripe checkout session for subscription.

    Requires authentication.
    """
    # Verify token
    payload = auth_service.verify_token(request.token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload["sub"])
    email = payload["email"]

    # Create checkout session
    try:
        session_id = stripe_service.create_checkout_session(
            user_id=user_id,
            email=email,
            plan_type=request.plan_type
        )

        # Get session URL
        import stripe
        checkout_session = stripe.checkout.Session.retrieve(session_id)

        return CheckoutResponse(
            session_id=session_id,
            url=checkout_session.url
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Checkout creation failed: {str(e)}"
        )


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    session: Session = Depends(get_session)
):
    """
    Handle Stripe webhooks.

    Processes subscription events.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing signature")

    success = stripe_service.handle_webhook(payload, sig_header, session)

    if not success:
        raise HTTPException(status_code=400, detail="Invalid webhook")

    return {"status": "success"}
