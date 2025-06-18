from typing import Sequence, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.users import Users
from db.session import async_session_maker


class UserRepository:

    @staticmethod
    async def add_user(session: AsyncSession, user: Users) -> None:
        session.add(user)
        await session.commit()

    @staticmethod
    async def update_user(session: AsyncSession, user_id: int, data: dict) -> None:
        user = await session.get(Users, user_id)
        for field, value in data.items():
            setattr(user, field, value)
        await session.commit()

    async def update_user_fields(self, session: AsyncSession, user_id: int, data: dict) -> None:
        user = await self.get_user_by_id(session, user_id)
        if user:
            for field, value in data.items():
                setattr(user, field, value)
            await session.commit()

    @staticmethod
    async def get_all_users() -> Sequence[Users]:
        async with async_session_maker() as session:
            query = select(Users)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int)-> Type[Users] | None:
        return await session.get(Users, user_id)

