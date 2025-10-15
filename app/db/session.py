from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.auth.config import settings  # adjust import if needed

# 1️⃣ Create async engine
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

# 2️⃣ Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# 3️⃣ Base class for models (optional if already defined elsewhere)
class Base(DeclarativeBase):
    pass

# 4️⃣ Dependency for FastAPI routes
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
