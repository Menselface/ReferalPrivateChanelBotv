from typing import Annotated

from sqlalchemy import BIGINT, String, Integer, DateTime, func, Boolean, false
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .users import Users


from ..base import Base

intpk = Annotated[int, mapped_column(primary_key=True)]

class Partners(Base):
    __tablename__ = "partners"

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    username: Mapped[str | None] = mapped_column(String(128))
    first_name: Mapped[str | None] = mapped_column(String(128))
    last_name: Mapped[str | None] = mapped_column(String(128))
    language_code: Mapped[str]
    has_accepted_terms: Mapped[bool] = mapped_column(Boolean, server_default=false(), nullable=False)

    ref_token: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    tribute_link: Mapped[str | None] = mapped_column(String(255))

    invites_total: Mapped[int] = mapped_column(Integer, default=0)
    invites_paid: Mapped[int] = mapped_column(Integer, default=0)
    invites_current: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    referred_users = relationship("Users", back_populates="referrer", cascade="all, delete")
