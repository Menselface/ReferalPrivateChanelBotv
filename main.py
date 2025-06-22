import logging

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command

from bot.handlers import accepted_terms, start_command_handler
from bot.handlers.admin import admin_router
from bot.handlers.chat_member import chat_member_router
from bot.handlers.commands import commands_router
from bot.handlers.registration_partner import registration_partner_router
from bot.middleware import DbSessionMiddleware
from bot.utils import logger, identify_myself
from sqlalchemy.ext.asyncio import AsyncSession


from config import config
from bot.utils import set_commands

bot = Bot(token=config.telegram.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
dp.message.middleware(DbSessionMiddleware())
dp.callback_query.middleware(DbSessionMiddleware())
dp.chat_member.middleware(DbSessionMiddleware())
dp.include_routers(chat_member_router,
                            accepted_terms,
                            commands_router,
                            admin_router,
                                registration_partner_router
                   )



@dp.message(Command('start'))
async def start_command(message: types.Message, bot: Bot, session: AsyncSession):
    await start_command_handler(message, bot, session)
    logger.info(f"user:{message.from_user.id} send command /start")




async def main():
    bot_info = await bot.get_me()
    logger.info(f"Бот @{bot_info.username} id={bot_info.id} - '{bot_info.first_name}' запустился")
    await set_commands(bot=bot)
    try:

        await bot.delete_webhook(drop_pending_updates=True)
        logger.info(f"Bot started from <y>{await identify_myself()}</y>")
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    import asyncio

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
