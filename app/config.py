from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MAILPIT_SMTP_HOST: str = "mailpit"
    MAILPIT_SMTP_PORT: int = 1025
    MAILPIT_API_URL: str = "http://mailpit:8025"
    MAILPIT_SENDER: str = "test@example.com"

    DATABASE_URL: str = "postgresql://user:password@db:5432/emaildb"

    class Config:
        env_file = ".env"

settings = Settings()