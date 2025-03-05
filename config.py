# app/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Advanced AI System"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database settings
    MONGODB_URL: str
    
    # API Keys
    OPENAI_API_KEY: str
    GOOGLE_API_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()
