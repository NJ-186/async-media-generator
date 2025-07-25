import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    DB_URL: str | None = os.getenv("DB_URL", "sqlite+aiosqlite:///./db.sqlite3")
    STORAGE_PATH: str = os.getenv("STORAGE_PATH", "./media")
    REPLICATE_API_TOKEN: str | None = os.getenv("REPLICATE_API_TOKEN")
    BROKER_URL: str = os.getenv("BROKER_URL", "redis://localhost:6379")
    RESULT_BACKEND: str = os.getenv("RESULT_BACKEND", "redis://localhost:6379/1")


settings = Settings()
