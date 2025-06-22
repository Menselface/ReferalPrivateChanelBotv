from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import config

def accept_terms_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="📄 Полное соглашение", url=config.agreements.conditions_link)
    builder.button(text="✅ Принять соглашение", callback_data="accept_terms")
    return builder.as_markup()