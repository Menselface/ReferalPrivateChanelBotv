
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.registration_partner import registration_first_step
from config import config
from locales import get_text
from services.partners_service import PartnersService

accepted_terms = Router(name=__name__)

@accepted_terms.callback_query(F.data == "accept_terms")
async def on_accept_rules(callback: CallbackQuery, session: AsyncSession, bot: Bot, state: FSMContext):
    user_id = callback.from_user.id
    await PartnersService().update_accept_rules(session, user_id, True)
    invite_link = await bot.create_chat_invite_link(
        chat_id=config.telegram.chat_id,
        name=f"ref_{user_id}",
        creates_join_request=False,
        member_limit=0,
    )
    await PartnersService().update_user_ref_link(session, user_id, invite_link.invite_link)
    logger.info(
        f"Пользователь {callback.from_user.username} {user_id=} принял соглашение"
    )
    await registration_first_step(callback.message, bot, state, user_id)


