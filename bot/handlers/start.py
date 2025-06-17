from aiogram import Bot
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession


from bot.keyboards import accept_terms_kb
from db.schemas.user import UserCreateDTO
from locales import get_text
from services.partners_service import PartnersService


async def start_command_handler(message: Message, bot: Bot, session: AsyncSession):
    user_id = message.from_user.id

    user = message.from_user
    user_dto = UserCreateDTO(
        user_id=user_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        language_code=user.language_code,
        ref_token=str(user_id)
    )
    await PartnersService().register_or_update_user(session, user_dto)

    if not await PartnersService().has_accepted_terms(session, user_id):
        await message.answer(
            get_text("rules"),
            reply_markup=accept_terms_kb(),
        )

    else:
        from bot.handlers.commands import check_user_stats
        await check_user_stats(message, bot, session)
