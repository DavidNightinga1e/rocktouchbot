import json
import os
from datetime import date
from typing import Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

CLIENTS_FILE = os.path.join(DATA_DIR, "clients.json")
ADMINS_FILE = os.path.join(DATA_DIR, "admins.json")


# ---------- helpers ----------

def _ensure_file(path: str, default_data: Dict[str, Any]) -> None:
    """Создаёт файл с дефолтным содержимым, если его нет"""
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8-sig") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)


def _load_json(path: str, default_data: Dict[str, Any]) -> Dict[str, Any]:
    _ensure_file(path, default_data)
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def _save_json(path: str, data: Dict[str, Any]) -> None:
    # атомарная запись
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8-sig") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)


def normalize_name(name: str) -> str:
    """Нормализует имя клиента (АнНа -> Анна)"""
    name = name.strip()
    if not name:
        return name
    return name[0].upper() + name[1:].lower()


# ---------- public API ----------

def load_clients() -> Dict[str, Any]:
    """
    Возвращает структуру:
    {
      "clients": {
        "Анна": {
          "visits_left": 5,
          "subscription_expires": "2026-03-25" | null
        }
      }
    }
    """
    return _load_json(CLIENTS_FILE, {"clients": {}})


def save_clients(data: Dict[str, Any]) -> None:
    _save_json(CLIENTS_FILE, data)


def load_admins() -> set[int]:
    """
    Возвращает set telegram_id администраторов
    """
    data = _load_json(ADMINS_FILE, {"admins": []})
    return set(data.get("admins", []))


# ---------- client helpers ----------

def client_exists(name: str) -> bool:
    name = normalize_name(name)
    data = load_clients()
    return name in data["clients"]


def get_client(name: str) -> Dict[str, Any] | None:
    name = normalize_name(name)
    data = load_clients()
    return data["clients"].get(name)


def add_client(name: str) -> None:
    name = normalize_name(name)
    data = load_clients()

    if name in data["clients"]:
        raise ValueError(f"Клиент '{name}' уже существует")

    data["clients"][name] = {
        "visits": 0,
        "expires": None
    }

    save_clients(data)


def update_client(name: str, client_data: Dict[str, Any]) -> None:
    name = normalize_name(name)
    data = load_clients()

    if name not in data["clients"]:
        raise ValueError(f"Клиент '{name}' не найден")

    data["clients"][name] = client_data
    save_clients(data)


def remove_client(name: str) -> None:
    name = normalize_name(name)
    data = load_clients()

    if name not in data["clients"]:
        raise ValueError(f"Клиент '{name}' не найден")

    data["clients"].pop(name)
    save_clients(data)