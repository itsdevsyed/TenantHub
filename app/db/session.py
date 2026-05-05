from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.auth.config import settings

# 🔗 Database engine (async)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True
)

# 🧠 Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# 🚪 FastAPI dependency
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session