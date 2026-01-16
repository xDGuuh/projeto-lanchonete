from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.models.base import Base

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/lanchonete"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

asyncSessionLocal = async_sessionmaker(
    engine, 
    expire_on_commit=False,
)