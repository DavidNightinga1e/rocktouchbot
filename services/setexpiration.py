from datetime import datetime, date

from services.storage import get_client, update_client


def set_client_expiration(name: str, expiration: date) -> None:
    """
    Ставит клиенту другую дату просрочки абонемента
    """
    client = get_client(name)

    if client is None:
        raise ValueError(f"Клиент '{name}' не найден")

    client["expires"] = expiration.isoformat()

    update_client(name, client)
