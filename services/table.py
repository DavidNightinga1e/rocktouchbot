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
        lines.append(f"{name}: {visits} (до {expires}, {days_until(expires)} дней)")

    return "\n".join(lines)
