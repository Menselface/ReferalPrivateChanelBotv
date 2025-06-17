from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="🚀 Start using the bot"),
        BotCommand(command="stats", description="📅 View your statistic info"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())

