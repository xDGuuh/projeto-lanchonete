import os
from dotenv import load_dotenv

load_dotenv()

# =====================
# Application
# =====================
APP_NAME: str = os.getenv("APP_NAME", "Projeto Lanchonete")
ENV: str = os.getenv("ENV", "development")
DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

# =====================
# Database
# =====================
DATABASE_URL: str | None = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

ASYNC_DATABASE_URL: str = DATABASE_URL.replace(
    "postgresql://",
    "postgresql+asyncpg://",
)

# =====================
# Server
# =====================
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", 8000))
