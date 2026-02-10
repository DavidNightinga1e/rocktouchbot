from datetime import date
from dateutil.relativedelta import relativedelta

from services.storage import (
    get_client,
    update_client,
    normalize_name,
)


def pay_subscription(name: str, visits: int) -> dict:
    """
    Добавляет посещения и продлевает абонемент на 2 месяца.
    Возвращает обновлённые данные клиента.
    """
    if visits <= 0:
        raise ValueError("Количество посещений должно быть больше 0")

    name = normalize_name(name)
    client = get_client(name)

    if client is None:
        raise ValueError(f"Клиент '{name}' не найден")

    new_expires = date.today() + relativedelta(months=2)

    client["visits"] += visits
    client["expires"] = new_expires.isoformat()

    update_client(name, client)
    return client
