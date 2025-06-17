
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from locales import get_text
from services.partners_service import PartnersService

accepted_terms = Router(name=__name__)

@accepted_terms.callback_query(F.data == "accept_terms")
async def on_accept_rules(callback: CallbackQuery, session: AsyncSession, bot: Bot):
    user_id = callback.from_user.id
    await PartnersService().update_accept_rules(session, user_id, True)
    invite_link = await bot.create_chat_invite_link(
        chat_id=config.telegram.chat_id,
        name=f"ref_{user_id}",
        creates_join_request=False,
        member_limit=0,
    )
    await PartnersService().update_user_ref_link(session, user_id, invite_link.invite_link)

    user_result_text = (
        f"{get_text('thank_you')}\n\nВаша ссылка: <code>{invite_link.invite_link}</code>"
    )
    await callback.message.edit_text(user_result_text, disable_web_page_preview=True)
    await callback.answer()
    logger.info(f"Пользователь {callback.from_user.username} {user_id=} принял соглашение")
