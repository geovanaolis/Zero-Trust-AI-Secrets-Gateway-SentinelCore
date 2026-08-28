from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src.infrastructure.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)

async def init_db():
    """Cria as tabelas no banco de dados se não existirem."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    """Dependency Injection para sessões assíncronas no FastAPI."""
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session