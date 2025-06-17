from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from services import AdminGetData, AdminEdit
from services.partners_service import PartnersService

admin_router = Router(name=__name__)


@admin_router.message(F.text.lower() == "админ")
async def admin_command(message: Message, bot: Bot, session: AsyncSession):
    user_id = message.from_user.id
    if not await PartnersService().check_user_is_admin(user_id=user_id):
        return

    admin_text = (
        "👨‍💻 <b>Административные команды:</b>\n\n"
        "• <code>/all_partners</code> — список партнёров с их статистикой 📊\n"
        "• <code>/edit_invites [user id] [число]</code> — корректировка счётчиков вручную ✏️\n\n"
        "<i>Пример использования:</i>\n"
        "<code>/edit_invites 563500589 5</code>"
    )

    await bot.send_message(
        user_id,
        admin_text
    )


@admin_router.message(Command("all_partners"))
async def all_partners_handler(message: Message, session: AsyncSession):
    if not await PartnersService.check_user_is_admin(message.from_user.id):
        return await message.answer("Нет доступа.")

    data = await AdminGetData().get_all_partners_stats(session)
    for block in data:
        await message.answer(block)

@admin_router.message(Command("edit_invites"))
async def edit_invites_handler(message: Message, session: AsyncSession):
    user_id = message.from_user.id
    if not await PartnersService.check_user_is_admin(user_id):
        return await message.answer("Нет доступа.")

    try:
        _, username, value = message.text.split()
        value = int(value)
    except Exception:
        return await message.answer("Неверный формат. Пример: /edit_invites 546645654 5")

    response = await AdminEdit().edit_invites_paid(session, user_id, value)
    await message.answer(response)
