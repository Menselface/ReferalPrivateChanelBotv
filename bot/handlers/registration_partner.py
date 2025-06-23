from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession


from locales import get_text
from services.partners_service import PartnersService

registration_partner_router = Router(name=__name__)

class EventStates(StatesGroup):
    awaiting_tribute_link = State()
    awaiting_second_tribute_link = State()

@registration_partner_router.message(Command(commands="change_tribute_link"))
async def registration_first_step(message: Message, bot: Bot, state: FSMContext, user_id: int = None):
    if not user_id:
        user_id = message.from_user.id
    registration_text = get_text('registration_text')
    await bot.send_message(
        user_id,
        registration_text
    )
    await state.set_state(EventStates.awaiting_tribute_link)



@registration_partner_router.message(EventStates.awaiting_tribute_link)
async def get_tribute_link_and_storage_to_table(message: Message, session: AsyncSession, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    tribute_link = message.text
    logger.info(f"User {user_id} send link {message.text}")
    await PartnersService().update_tribute_link(session, user_id, tribute_link)
    registration_text = get_text('registration_second_step')
    await bot.send_message(user_id, registration_text)
    await state.set_state(EventStates.awaiting_second_tribute_link)




@registration_partner_router.message(EventStates.awaiting_second_tribute_link)
async def get_tribute_link_and_storage_to_table(message: Message, session: AsyncSession, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    tribute_link = message.text
    logger.info(f"User {user_id} send second link {message.text}")
    await PartnersService().update_tribute_link_2(session, user_id, tribute_link)
    await state.clear()
    from bot.handlers.commands import check_user_stats
    await check_user_stats(message, bot, session)