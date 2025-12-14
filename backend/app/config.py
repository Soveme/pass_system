import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://pass_admin:secure_password@localhost:5432/pass_system"
    )
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "change_me_in_production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Encryption
    encryption_key: str = os.getenv("ENCRYPTION_KEY", "0" * 32)
    
    # CORS
    cors_origins: list = ["http://localhost:5173", "http://localhost:3000"]
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
