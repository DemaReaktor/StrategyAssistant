from telebot import TeleBot
from aiogram import types
from Dispatcher import dispatcher
import Config

bot = TeleBot(Config.BOT_TOKEN)

@bot.message_handler(commands=["start"])
def cmd_start(message):
    """Function to handle the /start command"""
    bot.reply_to(message, "Привіт, " + message.from_user.first_name)
