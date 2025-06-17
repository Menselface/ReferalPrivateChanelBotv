import asyncio

from sqlalchemy import text

from db.base import Base
from db.session import engine
from db.models.partners import Partners
from db.models.users import Users


from sqlalchemy import text

class AsyncCreateTables:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            print("Dropping all tables...")
            # Удаляем таблицы с CASCADE
            await conn.execute(text("DROP TABLE IF EXISTS users, partners CASCADE"))
            print("Creating all tables...")
            await conn.run_sync(Base.metadata.create_all)

async_core = AsyncCreateTables()

async def main():
    await async_core.create_tables()


if __name__ == "__main__":
    asyncio.run(main())
