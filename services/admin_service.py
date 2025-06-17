from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories.partners import PartnersRepository


class AdminBase:
    def __init__(self):
        self.partner_repo = PartnersRepository()


class AdminGetData(AdminBase):
    async def get_all_partners_stats(self, session: AsyncSession) -> list[str]:
        partners = await self.partner_repo.get_all_partners(session)
        if not partners:
            return ["Нет зарегистрированных партнёров."]

        result = []
        for p in partners:
            result.append(
                f"👤 {p.username or p.first_name or p.last_name} | <code>{p.user_id}</code>\n"
                f"📨 Всего: {p.invites_total}, 💸 Подписались: {p.invites_paid}, ✅ Активны: {p.invites_current}"
            )
        return result


class AdminEdit(AdminBase):
    async def edit_invites_paid(self, session: AsyncSession, user_id: int, value: int) -> str:
        partner = await self.partner_repo.get_partner_by_id(session, user_id)
        if not partner:
            return f"Партнёр с user_id '{user_id}' не найден."

        await self.partner_repo.update_partner_fields(session, user_id, {"invites_paid": value})
        return f"Обновлено: {user_id} → invites_paid = {value}"
