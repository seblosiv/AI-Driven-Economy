"""
Authentication service for magic links and OAuth.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select
from app.backend.models.user import User
from app.backend.core.config import settings


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Handle authentication logic."""

    def create_access_token(
        self,
        user_id: int,
        email: str,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT access token.

        Args:
            user_id: User ID
            email: User email
            expires_delta: Token expiration time

        Returns:
            Encoded JWT token
        """
        if expires_delta is None:
            expires_delta = timedelta(
                minutes=settings.access_token_expire_minutes
            )

        expire = datetime.utcnow() + expires_delta
        to_encode = {
            "sub": str(user_id),
            "email": email,
            "exp": expire
        }

        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm
        )
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[dict]:
        """
        Verify JWT token.

        Args:
            token: JWT token string

        Returns:
            Decoded payload or None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm]
            )
            return payload
        except JWTError:
            return None

    def get_or_create_user(
        self,
        session: Session,
        email: str,
        full_name: Optional[str] = None,
        oauth_provider: Optional[str] = None,
        oauth_id: Optional[str] = None
    ) -> User:
        """
        Get existing user or create new one.

        Args:
            session: Database session
            email: User email
            full_name: User's full name (optional)
            oauth_provider: OAuth provider name (optional)
            oauth_id: OAuth provider user ID (optional)

        Returns:
            User instance
        """
        # Check if user exists
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        if user:
            # Update last login
            user.last_login = datetime.utcnow()
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

        # Create new user
        user = User(
            email=email,
            full_name=full_name,
            oauth_provider=oauth_provider,
            oauth_id=oauth_id,
            is_active=True,
            last_login=datetime.utcnow()
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def send_magic_link(self, email: str) -> str:
        """
        Generate magic link token for passwordless auth.

        In production, this would send an email via Resend.
        For MVP, we return the token directly.

        Args:
            email: User email

        Returns:
            Magic link token
        """
        # Create short-lived token (15 minutes)
        expires_delta = timedelta(minutes=15)
        expire = datetime.utcnow() + expires_delta

        to_encode = {
            "sub": email,
            "type": "magic_link",
            "exp": expire
        }

        token = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm
        )

        # TODO: In production, send via Resend
        # resend.emails.send({
        #     "from": settings.from_email,
        #     "to": email,
        #     "subject": "Your Life After AI Login Link",
        #     "html": f"<a href='{settings.frontend_url}/auth/verify?token={token}'>Click to login</a>"
        # })

        return token

    def verify_magic_link(self, token: str) -> Optional[str]:
        """
        Verify magic link token.

        Args:
            token: Magic link token

        Returns:
            Email if valid, None otherwise
        """
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm]
            )

            if payload.get("type") != "magic_link":
                return None

            return payload.get("sub")  # Email
        except JWTError:
            return None


# Global auth service instance
auth_service = AuthService()
