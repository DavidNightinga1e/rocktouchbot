from telebot import TeleBot
from utils.permissions import init_permissions
from handlers.admin import register_admin_handlers
from handlers.public import register_public_handlers
from dotenv import dotenv_values


print("Loading env")
config = dotenv_values()

print("Creating bot")
TOKEN = config["TELEGRAM_TOKEN"]
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found in .env")

bot = TeleBot(TOKEN)

print("Init permissions")
# загружаем админов ОДИН РАЗ
init_permissions()

print("Registering handlers: admin")
register_admin_handlers(bot)
print("Registering handlers: public")
register_public_handlers(bot)

print("Starting bot")
bot.infinity_polling(skip_pending=True)