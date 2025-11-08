"""
Database session management.
"""
from typing import Generator
from sqlmodel import Session, create_engine
from app.backend.core.config import settings

# Create engine
engine = create_engine(
    settings.database_url,
    echo=not settings.is_production,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.

    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session


def init_db() -> None:
    """
    Initialize database tables.
    Creates all tables defined in SQLModel models.
    """
    from app.backend.db.base import SQLModel
    SQLModel.metadata.create_all(engine)
