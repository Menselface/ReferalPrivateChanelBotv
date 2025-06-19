from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="🚀 Начать работу с ботом"),
        BotCommand(command="stats", description="📊 Посмотреть свою статистику"),
        BotCommand(
            command="change_tribute_link",
            description="🔗 Изменить ссылку трибьют",
        ),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())

