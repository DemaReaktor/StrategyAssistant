from telebot import TeleBot
# from Dispatcher import dispatcher
from Handlers import bot
# from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
# from aiogram.types.inline_keyboard_button import InlineKeyboardButton
import json
import asyncio

if __name__ == "__main__":
    asyncio.run(bot.polling(none_stop=True, interval=0))
