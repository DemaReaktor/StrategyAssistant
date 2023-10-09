from telebot import TeleBot
from Handlers import bot
import asyncio

if __name__ == "__main__":
    asyncio.run(bot.polling(none_stop=True, interval=0))
