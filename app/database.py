"""
Database connection with async SQLAlchemy.

Async database operations provide better performance under load
by not blocking the event loop during I/O operations.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import get_settings

settings = get_settings()

# Create async engine
# pool_pre_ping=True ensures connections are valid before use
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Create async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    
    Using DeclarativeBase is the recommended approach
    in SQLAlchemy 2.0+.
    """
    pass


async def get_db() -> AsyncSession:
    """
    Dependency that provides async database session.
    
    Usage in endpoints:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    
    The session is automatically closed after the request.
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
