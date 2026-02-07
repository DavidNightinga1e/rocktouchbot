from typing import Set
from services.storage import load_admins

_admins: Set[int] = set()


def init_permissions() -> None:
    """
    Загружает список администраторов в память.
    Вызывать один раз при старте бота.
    """
    global _admins
    _admins = load_admins()


def is_admin(user_id: int) -> bool:
    """
    Проверяет, является ли пользователь администратором (in-memory)
    """
    return user_id in _admins


def require_admin(bot, message) -> bool:
    """
    Проверка прав для handler'ов.
    """
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "⛔ У тебя нет прав для этой команды")
        return False
    return True
