from services.storage import load_clients
from utils.dateutils import days_until


def format_clients_table() -> str:
    """
    Возвращает красивую таблицу всех клиентов с оставшимися посещениями
    и датой окончания абонемента
    """
    clients = load_clients()["clients"]
    if not clients:
        return "Список клиентов пуст."

    lines = []
    for name, data in clients.items():
        visits = data.get("visits", 0)
        expires = data.get("expires", "не указан")
        color_prefix = "💚" if visits > 2 else "💛" if visits > 0 else "💔"
        expiration_info = f"(до {expires}, {days_until(expires)} дней)" if expires else ""
        lines.append(f"{color_prefix} {name}: <b>{visits}</b> {expiration_info}")

    return "\n".join(lines)
