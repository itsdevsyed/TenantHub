# app/auth/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.auth.config import settings  # adjust import if needed

# 1️⃣ Create async engine
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

# 2️⃣ Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# 3️⃣ Dependency for FastAPI routes
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session