# import logging
#
# from aiogram import Bot, Dispatcher
# from aiogram.enums.parse_mode import ParseMode
# from aiogram.fsm.storage.memory import MemoryStorage
#
# import Config
#
# # Configure logging
# logging.basicConfig(level=logging.INFO)
#
# # prerequisites
# if not Config.BOT_TOKEN:
#     exit("No token provided")
#
# # init
# bot = Bot(token=Config.BOT_TOKEN, parse_mode=ParseMode.HTML)
# dispatcher = Dispatcher(storage=MemoryStorage())
