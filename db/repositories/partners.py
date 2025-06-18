from typing import Sequence, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.partners import Partners


class PartnersRepository:

    @staticmethod
    async def add_partner(session: AsyncSession, partner: Partners) -> None:
        session.add(partner)
        await session.commit()

    @staticmethod
    async def update_partner(session: AsyncSession, user_id: int, data: dict) -> None:
        user = await session.get(Partners, user_id)
        for field, value in data.items():
            setattr(user, field, value)
        await session.commit()

    async def update_partner_fields(self, session: AsyncSession, user_id: int, data: dict) -> None:
        user = await self.get_partner_by_id(session, user_id)
        if user:
            for field, value in data.items():
                setattr(user, field, value)
            await session.commit()

    @staticmethod
    async def get_all_partners(session: AsyncSession) -> Sequence[Partners]:
        result = await session.execute(select(Partners))
        return result.scalars().all()

    @staticmethod
    async def get_partner_by_id(session: AsyncSession, user_id: int)-> Type[Partners] | None:
        return await session.get(Partners, user_id)

    @staticmethod
    async def get_by_invite_link(session: AsyncSession, link: str):
        stmt = select(Partners).where(Partners.tribute_link == link)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

class PartnerStats(PartnersRepository):

    @staticmethod
    async def increment_invites_total(session: AsyncSession, user_id: int):
        user =  await session.get(Partners, user_id)
        if not user:
            return
        user.invites_total += 1
        await session.commit()

    @staticmethod
    async def increment_invites_paid(session: AsyncSession, user_id: int):
        user = await session.get(Partners, user_id)
        if not user:
            return
        user.invites_paid += 1
        await session.commit()

    @staticmethod
    async def   increment_invites_current(session: AsyncSession, user_id: int):
        user = await session.get(Partners, user_id)
        if not user:
            return
        user.invites_current += 1
        await session.commit()

    @staticmethod
    async def decrement_invites_current(session: AsyncSession, user_id: int):
        user =  await session.get(Partners, user_id)
        if not user:
            return
        if user.invites_current > 0:
            user.invites_current -= 1
            await session.commit()