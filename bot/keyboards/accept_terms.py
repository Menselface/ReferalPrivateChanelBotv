from aiogram.utils.keyboard import InlineKeyboardBuilder

def accept_terms_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="📄 Полное соглашение", url='google.com')
    builder.button(text="✅ Принять соглашение", callback_data="accept_terms")
    return builder.as_markup()