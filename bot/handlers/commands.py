from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers import start_command_handler
from services.partners_service import PartnersService, GetPartner

commands_router = Router(name=__name__)

@commands_router.message(Command(commands="stats"))
async def check_user_stats(message: Message, bot: Bot, session: AsyncSession):
    user_id = message.from_user.id
    if not await PartnersService().has_accepted_terms(session, user_id):
        await start_command_handler(message, bot, session)

    else:
        user_stats = await GetPartner().get_user_statistic(session, user_id)
        await bot.send_message(user_id, user_stats)