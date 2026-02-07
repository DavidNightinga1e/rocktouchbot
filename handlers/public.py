from telebot import TeleBot
from services.table import format_clients_table
from utils.permissions import is_admin
from utils.safehandler import safe_handler


def register_public_handlers(bot: TeleBot):

    @bot.message_handler(commands=['table'])
    @safe_handler(bot)
    def table_handler(message):
        table_text = format_clients_table()
        bot.reply_to(message, f"📋 Текущие посещения:\n\n{table_text}")

    @bot.message_handler(commands=['info'])
    @safe_handler(bot)
    def info_handler(message):
        user_id = message.from_user.id
        admin = is_admin(user_id)

        lines = ["📌 Доступные команды:\n"]

        # Команды для всех пользователей
        lines.append("**/table** — показать текущие посещения всех клиентов\n"
                     "Пример: /table")

        lines.append("**/info** — показать доступные команды\n"
                     "Пример: /info")

        if admin:
            lines.append("\n⚙ **Команды администратора:**")
            lines.append("**/add Имя** — добавить нового клиента\n"
                         "Пример: /add Анна")
            lines.append("**/pay Имя Количество** — добавить посещения и продлить абонемент на 2 месяца\n"
                         "Пример: /pay Анна 10")
            lines.append("**/train ИмяКоличество ИмяКоличество ...** — списать посещения (можно отрицательное для возврата или не указывать количество - по-умолчанию 1)\n"
                         "Пример: /train Анна Иван2 Олег-1")

        bot.reply_to(message, "\n\n".join(lines), parse_mode="Markdown")
