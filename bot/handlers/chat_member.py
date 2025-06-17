from aiogram import Router, Bot
from aiogram.types import ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories.partners import PartnersRepository

chat_member_router = Router(name=__name__)



@chat_member_router.chat_member()
async def on_join(event: ChatMemberUpdated, session: AsyncSession, bot: Bot):
    partner_repo = PartnersRepository()
    if event.new_chat_member.status == "member":
        if event.invite_link:
            user = event.from_user
            ref_link = event.invite_link.invite_link
            partner = await partner_repo.get_by_invite_link(session, ref_link)
            if partner:
                await partner_repo.increment_paid(session, partner.user_id)
                await bot.send_message(partner.user_id, f"🎉 {user.username or user.id} вступил по вашей ссылке!")
