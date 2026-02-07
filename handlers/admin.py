from telebot import TeleBot

from services.payments import pay_subscription
from services.storage import add_client, normalize_name
from services.trainings import train_clients, parse_train_arg
from utils.permissions import require_admin
from utils.safehandler import safe_handler


def register_admin_handlers(bot: TeleBot):

    @bot.message_handler(commands=['add'])
    @safe_handler(bot)
    def add_client_handler(message):
        if not require_admin(bot, message):
            return

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            bot.reply_to(message, "⚠ Использование: /add Имя")
            return

        raw_name = parts[1].strip()

        if not raw_name.isalpha():
            bot.reply_to(
                message,
                "⚠ Имя должно состоять только из букв\n"
                "Пример: /add Анна"
            )
            return

        name = normalize_name(raw_name)

        try:
            add_client(name)
        except ValueError as e:
            bot.reply_to(message, f"⚠ {e}")
            return

        bot.reply_to(
            message,
            f"✅ Клиент *{name}* успешно добавлен\n"
            "Посещений: 0\n"
            "Абонемент: отсутствует",
            parse_mode="Markdown"
        )

    @bot.message_handler(commands=['pay'])
    @safe_handler(bot)
    def pay_handler(message):
        if not require_admin(bot, message):
            return

        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(
                message,
                "⚠ Использование: /pay Имя Количество\n"
                "Пример: /pay Анна 10"
            )
            return

        _, raw_name, raw_visits = parts

        if not raw_visits.isdigit():
            bot.reply_to(message, "⚠ Количество посещений должно быть числом")
            return

        visits = int(raw_visits)

        try:
            client = pay_subscription(raw_name, visits)
        except ValueError as e:
            bot.reply_to(message, f"⚠ {e}")
            return

        bot.reply_to(
            message,
            f"✅ Оплата принята\n\n"
            f"Клиент: *{raw_name.capitalize()}*\n"
            f"Добавлено посещений: {visits}\n"
            f"Всего осталось: {client['visits']}\n"
            f"Абонемент до: {client['expires']}",
            parse_mode="Markdown"
        )

    @bot.message_handler(commands=['train'])
    @safe_handler(bot)
    def train_handler(message):
        if not require_admin(bot, message):
            return

        parts = message.text.split()[1:]
        if not parts:
            bot.reply_to(
                message,
                "⚠ Использование: /train Имя[Количество] ...\n"
                "Пример: /train Анна Иван2 (Анна была одна, Иван со своим +1)"
            )
            return

        clients_with_counts = {}
        for arg in parts:
            name, count = parse_train_arg(arg)
            if not name or count == 0:
                bot.reply_to(
                    message,
                    f"⚠ Неверный формат: {arg}\n"
                    "Пример: Иван3, Анна или Олег-2 (количество не 0)"
                )
                return
            clients_with_counts[name] = count

        results = train_clients(clients_with_counts)

        # Проверяем ошибки
        if any(not res["success"] for res in results.values()):
            error_lines = [
                f"⚠ {name}: {res['error']}"
                for name, res in results.items() if not res["success"]
            ]
            bot.reply_to(
                message,
                "⚠ Операция отменена из-за ошибок:\n" + "\n".join(error_lines)
            )
            return

        # Формируем отчёт
        response_lines = []

        for name, res in results.items():
            change = clients_with_counts[name]
            if change < 0:
                action = "пополнено"
                change_display = abs(change)
            else:
                action = "списано"
                change_display = change

            response_lines.append(
                f"✅ {name}: {action} {change_display}, осталось {res['visits']}"
            )

        bot.reply_to(message, "\n".join(response_lines))