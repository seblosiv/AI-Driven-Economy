"""
Database base configuration and utilities.
"""
from sqlmodel import SQLModel

# Import all models here to ensure they're registered with SQLModel
# This is needed for Alembic migrations and create_all()
from app.backend.models.user import User  # noqa: F401
from app.backend.models.occupation import Occupation  # noqa: F401
from app.backend.models.quiz import QuizResponse  # noqa: F401
from app.backend.models.prediction import AutomationPrediction  # noqa: F401
from app.backend.models.subscription import Subscription  # noqa: F401

__all__ = ["SQLModel"]
