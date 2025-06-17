import datetime
from typing import Annotated

from sqlalchemy import String, BIGINT, text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


from db.base import Base

created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow(),)]

class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    username: Mapped[str | None] = mapped_column(String(128))
    first_name: Mapped[str | None] = mapped_column(String(128))
    last_name: Mapped[str | None] = mapped_column(String(128))

    ref_by: Mapped[int | None] = mapped_column(BIGINT, ForeignKey("partners.user_id"), nullable=True)
    joined_paid_channel: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)  # true, если всё ещё в канале

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    referrer = relationship("Partners", back_populates="referred_users")

