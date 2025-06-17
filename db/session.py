from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config import config

engine = create_async_engine(
        url=config.db.host_url,
        echo=False
    )
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
