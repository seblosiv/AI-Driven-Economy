"""
Subscription model for Stripe integration.
"""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Subscription(SQLModel, table=True):
    """User subscription tracking."""

    __tablename__ = "subscriptions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)

    # Stripe data
    stripe_customer_id: str = Field(max_length=255, index=True)
    stripe_subscription_id: Optional[str] = Field(default=None, max_length=255, index=True)
    stripe_price_id: Optional[str] = Field(default=None, max_length=255)

    # Subscription details
    status: str = Field(max_length=50)  # active, canceled, past_due, etc.
    plan_type: str = Field(max_length=50)  # monthly, yearly

    # Dates
    current_period_start: Optional[datetime] = Field(default=None)
    current_period_end: Optional[datetime] = Field(default=None)
    canceled_at: Optional[datetime] = Field(default=None)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "stripe_customer_id": "cus_123",
                "status": "active",
                "plan_type": "monthly"
            }
        }
