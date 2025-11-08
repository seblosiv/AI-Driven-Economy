"""
User model for authentication and profile.
"""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User model with authentication and subscription info."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    full_name: Optional[str] = Field(default=None, max_length=255)

    # Auth
    hashed_password: Optional[str] = Field(default=None, max_length=255)
    oauth_provider: Optional[str] = Field(default=None, max_length=50)  # google, etc.
    oauth_id: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)

    # Subscription
    is_pro: bool = Field(default=False)
    subscription_id: Optional[str] = Field(default=None, max_length=255)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = Field(default=None)

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "full_name": "Jane Doe",
                "is_pro": False
            }
        }
