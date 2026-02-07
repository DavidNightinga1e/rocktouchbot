from services.storage import get_client, update_client, normalize_name
import re

# Теперь число может быть отрицательным
TRAIN_RE = re.compile(r"^([A-Za-zА-Яа-яёЁ]+)(-?\d*)$")

def parse_train_arg(arg: str):
    """
    Возвращает (имя, количество)
    Примеры:
      'Иван2' -> ('Иван', 2)
      'Анна' -> ('Анна', 1)
      'Олег-2' -> ('Олег', -2)
    """
    match = TRAIN_RE.match(arg.strip())
    if not match:
        return None, None
    name = normalize_name(match.group(1))
    count_str = match.group(2)
    count = int(count_str) if count_str else 1
    return name, count


def train_clients(clients_with_counts: dict) -> dict:
    """
    clients_with_counts: {"Анна": 1, "Иван": 2, ...}

    Транзакционная обработка:
    - Если любой клиент не найден → операция отменяется
    - Отрицательное количество посещений после списания допустимо
    """
    results = {}

    # ---------- 1. Валидация ----------
    for raw_name in clients_with_counts:
        name = normalize_name(raw_name)
        client = get_client(name)
        if client is None:
            results[name] = {"success": False, "error": f"Клиент '{name}' не найден"}

    if any(not res["success"] for res in results.values()):
        # ---------- откат ----------
        return results

    # ---------- 2. Обновление ----------
    for raw_name, count in clients_with_counts.items():
        name = normalize_name(raw_name)
        client = get_client(name)
        client["visits"] -= count  # отрицательное visits допустимо
        update_client(name, client)
        results[name] = {"success": True, "visits": client["visits"]}

    return results
