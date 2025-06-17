from datetime import datetime, timezone

from aiogram import Bot
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from db.models.users import Users
from db.repositories.users import UserRepository
from db.schemas.user import UserCreateDTO
from locales import get_text


class UserService:

    def __init__(self):
        self.repo = UserRepository()

    async def register_or_update_user(self, session: AsyncSession, user_data: UserCreateDTO):
        existing_user = await self.repo.get_user_by_id(session, user_data.user_id)

        if existing_user:
            await self.repo.update_user(session, user_data.user_id, user_data.model_dump())
        else:
            new_user = Users(**user_data.model_dump())
            await self.repo.add_user(session, new_user)


    async def has_accepted_terms(self, session: AsyncSession, user_id: int):
        user = await self.repo.get_user_by_id(session, user_id)
        return user.has_accepted_terms if user else False


    async def update_accept_rules(self, session: AsyncSession, user_id: int, value: bool):
        await self.repo.update_user_fields(session, user_id, {"has_accepted_terms": value})


    @staticmethod
    async def check_user_is_admin(user_id: int):
        admins_list = config.telegram.admins
        return False if user_id not in admins_list else True




