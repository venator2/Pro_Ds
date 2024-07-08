import telegram
from django.conf import settings


def send_telegram_message(message):
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=message)