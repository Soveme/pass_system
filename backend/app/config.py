import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:secure_password_2025@localhost:5432/postgres"
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
    cors_origins: list = ["http://localhost:5173", "http://localhost:3000", "https://qdgj4u-5-140-6-221.ru.tuna.am", "https://brqj3q-5-140-6-221.ru.tuna.am", "https://vo9ksn-5-140-6-221.ru.tuna.am"]
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
