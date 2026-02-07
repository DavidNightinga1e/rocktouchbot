from datetime import datetime, date


def parse_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def days_until(date_str: str) -> int | None:
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