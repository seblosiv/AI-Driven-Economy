"""
Stripe integration for payments and subscriptions.
"""
from typing import Optional
from datetime import datetime
import stripe
from sqlmodel import Session, select
from app.backend.models.user import User
from app.backend.models.subscription import Subscription
from app.backend.core.config import settings


class StripeService:
    """Handle Stripe payments and subscriptions."""

    def __init__(self):
        """Initialize Stripe."""
        if settings.stripe_secret_key:
            stripe.api_key = settings.stripe_secret_key

    def create_checkout_session(
        self,
        user_id: int,
        email: str,
        plan_type: str = "monthly"
    ) -> str:
        """
        Create Stripe checkout session for subscription.

        Args:
            user_id: User ID
            email: User email
            plan_type: "monthly" or "yearly"

        Returns:
            Checkout session ID
        """
        # Determine price ID
        if plan_type == "yearly":
            price_id = settings.stripe_price_id_yearly
        else:
            price_id = settings.stripe_price_id_monthly

        # Create checkout session
        session = stripe.checkout.Session.create(
            customer_email=email,
            client_reference_id=str(user_id),
            payment_method_types=['card'],
            mode='subscription',
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            success_url=f"{settings.frontend_url}/premium/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.frontend_url}/premium",
            metadata={
                'user_id': str(user_id),
                'plan_type': plan_type
            }
        )

        return session.id

    def handle_webhook(
        self,
        payload: bytes,
        sig_header: str,
        db_session: Session
    ) -> bool:
        """
        Handle Stripe webhook events.

        Args:
            payload: Raw request body
            sig_header: Stripe signature header
            db_session: Database session

        Returns:
            True if handled successfully
        """
        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.stripe_webhook_secret
            )
        except ValueError:
            return False
        except stripe.error.SignatureVerificationError:
            return False

        # Handle different event types
        if event['type'] == 'checkout.session.completed':
            self._handle_checkout_completed(event['data']['object'], db_session)
        elif event['type'] == 'customer.subscription.updated':
            self._handle_subscription_updated(event['data']['object'], db_session)
        elif event['type'] == 'customer.subscription.deleted':
            self._handle_subscription_deleted(event['data']['object'], db_session)

        return True

    def _handle_checkout_completed(
        self,
        session: dict,
        db_session: Session
    ) -> None:
        """Handle successful checkout."""
        user_id = int(session['metadata']['user_id'])
        plan_type = session['metadata']['plan_type']

        # Get user
        user = db_session.get(User, user_id)
        if not user:
            return

        # Create or update subscription
        subscription = Subscription(
            user_id=user_id,
            stripe_customer_id=session['customer'],
            stripe_subscription_id=session['subscription'],
            status='active',
            plan_type=plan_type
        )
        db_session.add(subscription)

        # Update user
        user.is_pro = True
        user.subscription_id = session['subscription']
        db_session.add(user)

        db_session.commit()

    def _handle_subscription_updated(
        self,
        subscription_data: dict,
        db_session: Session
    ) -> None:
        """Handle subscription updates."""
        stripe_sub_id = subscription_data['id']

        # Find subscription
        statement = select(Subscription).where(
            Subscription.stripe_subscription_id == stripe_sub_id
        )
        subscription = db_session.exec(statement).first()

        if subscription:
            subscription.status = subscription_data['status']
            subscription.updated_at = datetime.utcnow()
            db_session.add(subscription)
            db_session.commit()

    def _handle_subscription_deleted(
        self,
        subscription_data: dict,
        db_session: Session
    ) -> None:
        """Handle subscription cancellation."""
        stripe_sub_id = subscription_data['id']

        # Find subscription
        statement = select(Subscription).where(
            Subscription.stripe_subscription_id == stripe_sub_id
        )
        subscription = db_session.exec(statement).first()

        if subscription:
            subscription.status = 'canceled'
            subscription.canceled_at = datetime.utcnow()
            db_session.add(subscription)

            # Update user
            user = db_session.get(User, subscription.user_id)
            if user:
                user.is_pro = False
                db_session.add(user)

            db_session.commit()

    def get_portal_url(self, customer_id: str) -> str:
        """
        Create customer portal session.

        Args:
            customer_id: Stripe customer ID

        Returns:
            Portal URL
        """
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=f"{settings.frontend_url}/premium"
        )
        return session.url


# Global service instance
stripe_service = StripeService()
