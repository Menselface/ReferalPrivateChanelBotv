from aiogram import Router, Bot
from aiogram.types import ChatMemberUpdated
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from db.repositories.partners import PartnersRepository, PartnerStats
from db.schemas import UserInvitedCreateDTO
from services import UserService

chat_member_router = Router(name=__name__)


@chat_member_router.chat_member()
async def on_join_in_paid_channels(event: ChatMemberUpdated, session: AsyncSession, bot: Bot):
    user = event.from_user
    chat_id = event.chat.id
    status = event.new_chat_member.status
    if event.chat.id not in config.telegram.chat_paid_ids   :
        await on_join(event, session, bot)
        return

    if status == "member":
        user_service = UserService()
        partner_repo = PartnerStats()
        user_data = await user_service.repo.get_user_by_id(session, user.id)
        if user_data and user_data.ref_by and not user_data.joined_paid_channel:
            await partner_repo.increment_invites_paid(session, user_data.ref_by)
            await partner_repo.increment_invites_current(session, user_data.ref_by)
            await user_service.mark_paid_channel_joined(session, user.id)

            await bot.send_message(
                user_data.ref_by,
                f"💸 Пользователь {user.username or user.id} оплатил подписку!"
            )

    if status in ("left", "kicked") and chat_id in config.telegram.chat_paid_ids:
        user_service = UserService()
        partner_repo = PartnerStats()

        user_data = await user_service.repo.get_user_by_id(session, user.id)
        if user_data and user_data.ref_by:
            await partner_repo.decrement_invites_current(session, user_data.ref_by)
            await user_service.mark_user_inactive(session, user.id)



@chat_member_router.chat_member()
async def on_join(event: ChatMemberUpdated, session: AsyncSession, bot: Bot):
    partner_repo = PartnersRepository()
    logger.info(f"📍 Сообщение из чата: {event.chat.title} [{event.chat.id}]")
    if event.new_chat_member.status == "member":
        if event.invite_link:
            user = event.from_user
            ref_link = event.invite_link.invite_link
            partner = await partner_repo.get_by_invite_link(session, ref_link)
            if partner:
                user_dto = UserInvitedCreateDTO(
                    user_id=user.id,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    ref_by=partner.user_id
                )
                await PartnerStats().increment_invites_total(session, partner.user_id)
                await UserService().register_or_update_user(session, user_dto)
                await bot.send_message(partner.user_id, f"🎉 {user.username or user.id} вступил по вашей ссылке!")

