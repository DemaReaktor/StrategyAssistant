import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import Config

# Configure logging
logging.basicConfig(level=logging.INFO)

# prerequisites
if not Config.BOT_TOKEN:
    exit("No token provided")

# init
bot = Bot(token=Config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
