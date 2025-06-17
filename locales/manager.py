from locales import en
from locales import ru

LANGUAGES = {
    "en": en.texts,
    "ru": ru.texts,
}

DEFAULT_LANG = "ru"

def get_text(key: str, lang_code: str = 'ru') -> str:
    return LANGUAGES.get(lang_code, LANGUAGES[DEFAULT_LANG]).get(key, f"[Missing text: {key}]")
