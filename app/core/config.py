from pydantic import BaseModel
import os

class Settings(BaseModel):
    APP_ENV : str = os.getenv("APP_ENV", "dev")
    DATABASE_URL : str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change_me")
    JWT_ALG: str= os.getenv("JWT_ALG", "HS256")
    JWT_EXPIRES_MIN: int= int(os.getenv("JWT_EXPIRES_MIN", "60"))
    UPLOAD_DIR: str= os.getenv("UPLOAD_DIR", "./uploads")
    MAX_ATTACHMENT_MB: int = int(os.getenv("MAX_ATTACHMENT_MB", "5"))
    ALLOWED_MIME: str = os.getenv("ALLOWED_MIME", "image/png,image/jpeg,application/pdf")
    CORS_ORIGINS: str= os.getenv("CORS_ORIGINS", "http://localhost:5173")
    TZ_DEFAULT: str= os.getenv("TZ_DEFAULT", "UTC")


settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok = True)

