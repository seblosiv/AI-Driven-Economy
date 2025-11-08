"""
Application configuration management using Pydantic Settings.
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Database
    database_url: str = Field(
        default="sqlite:///./lifeafterai.db",
        description="Database connection URL"
    )

    # JWT & Auth
    secret_key: str = Field(
        default="dev-secret-key-change-in-production-please",
        description="Secret key for JWT token generation"
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        default=10080,  # 7 days
        description="Access token expiration in minutes"
    )

    # OAuth
    google_client_id: str = Field(default="", description="Google OAuth client ID")
    google_client_secret: str = Field(default="", description="Google OAuth client secret")

    # AI Provider
    openai_api_key: str = Field(default="", description="OpenAI API key")
    deepinfra_api_key: str = Field(default="", description="DeepInfra API key")
    groq_api_key: str = Field(default="", description="Groq API key")
    ai_provider: str = Field(
        default="local",
        description="AI provider: openai | deepinfra | groq | local"
    )

    # Stripe
    stripe_secret_key: str = Field(default="", description="Stripe secret key")
    stripe_publishable_key: str = Field(default="", description="Stripe publishable key")
    stripe_webhook_secret: str = Field(default="", description="Stripe webhook secret")
    stripe_price_id_monthly: str = Field(default="", description="Stripe monthly price ID")
    stripe_price_id_yearly: str = Field(default="", description="Stripe yearly price ID")

    # Email
    resend_api_key: str = Field(default="", description="Resend API key")
    from_email: str = Field(
        default="hello@lifeafterai.com",
        description="From email address"
    )

    # PostHog
    posthog_api_key: str = Field(default="", description="PostHog API key")
    posthog_host: str = Field(
        default="https://app.posthog.com",
        description="PostHog host URL"
    )

    # App URLs
    frontend_url: str = Field(
        default="http://localhost:5173",
        description="Frontend URL for CORS and redirects"
    )
    backend_url: str = Field(
        default="http://localhost:8000",
        description="Backend URL"
    )
    environment: str = Field(default="development", description="Environment name")

    # CORS
    cors_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        description="Comma-separated list of allowed CORS origins"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"


# Global settings instance
settings = Settings()
