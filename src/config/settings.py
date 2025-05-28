from functools import cache
from pydantic import PostgresDsn, RedisDsn, SecretStr, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Manages application settings loaded from environment variables."""

    # API Configuration
    API_V1_STR: str = "/api/v1"
    BASE_URL: str = "http://localhost:8000"
    APP_PORT: int = 8000

    # Project Metadata
    PROJECT_NAME: str = "FastAPI Project"
    PROJECT_DESCRIPTION: str = "A refactored FastAPI application."
    PROJECT_VERSION: str = "1.0.0"

    # PostgreSQL Database Credentials
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str
    POSTGRES_PORT: int  # Changed to int for proper type validation
    POSTGRES_DATABASE: str

    # Redis Cache & Message Broker Credentials
    REDIS_HOST: str
    REDIS_PORT: int  # Changed to int
    REDIS_DB: int = 0  # Changed to int

    # JWT Authentication Credentials
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    # Email Service Credentials
    EMAIL_PASSWORD: str
    EMAIL: str  # Use Pydantic's EmailStr for validation
    SMTP_PORT: int = 587
    SMTP_SERVER: str

    # Pydantic settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # Environment variables are typically case-insensitive
        extra="ignore",  # Ignore extra fields from .env
    )

    @property
    def postgres_dsn(self) -> str:
        return f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"

    @property
    def redis_url(self) -> str:
        """Constructs the Redis connection URL string."""
        # Use Pydantic's RedisDsn for validation if needed
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


@cache
def get_settings() -> Settings:
    """Returns a cached instance of the application settings."""
    # The @cache decorator ensures Settings is initialized only once.
    return Settings()  # noqa
