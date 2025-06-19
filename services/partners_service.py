from aiogram.types import ChatInviteLink
from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from db.models.partners import Partners
from db.repositories.partners import PartnersRepository
from db.schemas.user import UserCreateDTO


class PartnersService:

    def __init__(self):
        self.repo = PartnersRepository()

    async def register_or_update_user(self, session: AsyncSession, user_data: UserCreateDTO):
        existing_user = await self.repo.get_partner_by_id(session, user_data.user_id)

        if existing_user:
            return False
        else:
            new_user = Partners(**user_data.model_dump())
            await self.repo.add_partner(session, new_user)


    async def has_accepted_terms(self, session: AsyncSession, user_id: int):
        user = await self.repo.get_partner_by_id(session, user_id)
        return user.has_accepted_terms if user else False


    async def update_accept_rules(self, session: AsyncSession, user_id: int, value: bool):
        await self.repo.update_partner_fields(session, user_id, {"has_accepted_terms": value})

    async def update_user_ref_link(self, session: AsyncSession, user_id: int, invite_link: str):
        partner = await self.repo.get_partner_by_id(session, user_id)
        if not partner:
            return False

        await self.repo.update_partner_fields(
            session, user_id, {"ref_token": invite_link}
        )
        return partner.ref_token

    async def update_tribute_link(self, session: AsyncSession, user_id: int, invite_link: str):
        partner = await self.repo.get_partner_by_id(session, user_id)
        if not partner:
            return False

        await self.repo.update_partner_fields(
            session, user_id, {"tribute_link": invite_link}
        )
        return partner.tribute_link

    @staticmethod
    async def check_user_is_admin(user_id: int):
        admins_list = config.telegram.admins
        return False if user_id not in admins_list else True


class GetPartner(PartnersService):
    async def get_user_statistic(self, session: AsyncSession, user_id: int) -> str:
        partner = await self.repo.get_partner_by_id(session, user_id)
        if not partner:
            return "Вы ещё не зарегистрированы в системе."

        total = partner.invites_total
        paid = partner.invites_paid
        current = partner.invites_current
        user_ref = partner.ref_token

        return (
            "📊 <b>Ваша статистика:</b>\n\n"
            f"👥 Всего приглашено: <b>{total}</b>\n"
            f"💸 Оформили подписку: <b>{paid}</b>\n"
            f"✅ Сейчас активны: <b>{current}</b>\n\n"
            f"🔗 Ваша реферальная ссылка:\n"
            f"<code>{user_ref}</code>"
        )






