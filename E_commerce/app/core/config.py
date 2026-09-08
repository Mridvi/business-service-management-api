from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    UPLOAD_DIR: str = "uploads"
    MEDIA_URL_PREFIX: str = "/media"

    # Optional: comma-separated browser origins (e.g. https://app.example.com).
    # Leave empty to disable CORS (recommended for API-only / Postman / server clients).
    CORS_ALLOWED_ORIGINS: str = ""

    # Optional: base URL for password-reset links in emails (e.g. https://app.example.com).
    # If empty, the email includes the token for manual use via POST /auth/reset-password.
    PASSWORD_RESET_BASE_URL: str = ""

    class Config:
        env_file = ".env"

    @property
    def cors_origins(self) -> list[str]:
        if not self.CORS_ALLOWED_ORIGINS.strip():
            return []
        return [
            origin.strip()
            for origin in self.CORS_ALLOWED_ORIGINS.split(",")
            if origin.strip()
        ]


settings = Settings()
