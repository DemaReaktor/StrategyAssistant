from telebot import TeleBot
# from Dispatcher import dispatcher
from Handlers import bot
# from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
# from aiogram.types.inline_keyboard_button import InlineKeyboardButton
import json

if __name__ == "__main__":
    # buttons = [[InlineKeyboardButton(text='H',callback_data='f')]]
    # keyboard = InlineKeyboardMarkup(inline_keyboard=[[]])
    # json.dumps(keyboard)
    bot.polling(none_stop=True, interval=0)