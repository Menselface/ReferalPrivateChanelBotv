from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config import config


engine = create_async_engine(
    url=config.db.host_url,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=5,
    max_overflow=10
)

# Фабрика для сессий
async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
