from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path


class Settings(BaseSettings):
    PROJECT_NAME: str = "Noti Server"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    SQLITE_URL: str = "sqlite:///./noti.db"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]  # Frontend URL

    # Timezone
    TIMEZONE: str = "Asia/Shanghai"

    class Config:
        case_sensitive = True


settings = Settings()
