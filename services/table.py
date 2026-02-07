from services.storage import load_clients
from datetime import date
from datetime import datetime


def days_until(date_str: str) -> int:
    """
    Считает количество дней от сегодня до указанной даты.

    :param date_str: дата в формате "YYYY-MM-DD"
    :return: число дней (может быть отрицательным, если дата уже прошла)
    """
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.today().date()
        delta = target_date - today
        return delta.days
    except (ValueError, TypeError):
        return None  # если дата некорректная или пустая


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
