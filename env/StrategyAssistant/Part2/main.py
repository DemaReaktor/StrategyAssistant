from telebot import TeleBot
from Dispatcher import dispatcher
from Handlers import bot

if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)