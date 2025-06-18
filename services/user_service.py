from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from db.models.users import Users
from db.repositories.users import UserRepository
from db.schemas.user import UserInvitedCreateDTO


class UserService:

    def __init__(self):
        self.repo = UserRepository()

    async def register_or_update_user(self, session: AsyncSession, user_data: UserInvitedCreateDTO):
        existing_user = await self.repo.get_user_by_id(session, user_data.user_id)

        if existing_user:
            await self.repo.update_user(session, user_data.user_id, user_data.model_dump())
        else:
            new_user = Users(**user_data.model_dump())
            await self.repo.add_user(session, new_user)


    @staticmethod
    async def check_user_is_admin(user_id: int):
        admins_list = config.telegram.admins
        return False if user_id not in admins_list else True

    async def mark_paid_channel_joined(self, session: AsyncSession, user_id: int):
        await self.repo.update_user_fields(session, user_id, {
            "joined_paid_channel": True,
            "is_active": True
        })

    async def mark_user_inactive(self, session: AsyncSession, user_id: int):
        await self.repo.update_user_fields(session, user_id, {
            "is_active": False
        })




