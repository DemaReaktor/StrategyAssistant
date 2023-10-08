from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from Language import LanguageController
import json
class Keyboards:
    texts = {
        'що робить бот?': 'what does bot do',
        'суть стратегії?': 'logic of strategy',
        'як налаштувати стратегію?': 'how do adjust strategy',
        'які обмеження в стратегії?': 'which limits does strategy have',
    }
    LanguageController.add(texts)

    @staticmethod
    def main_keyboard(language):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text=language.translate('що робить бот?'),callback_data='що робить бот'))
        keyboard.add(InlineKeyboardButton(text=language.translate('суть стратегії?'),callback_data='суть стратегії'))
        keyboard.add(InlineKeyboardButton(text=language.translate('як налаштувати стратегію?'),
                                          callback_data='як налаштувати стратегію'))
        keyboard.add(InlineKeyboardButton(text=language.translate('які обмеження в стратегії?'),
                                          callback_data='які обмеження в стратегії'))
        return keyboard

    @staticmethod
    def strategy_keyboard(language):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text=language.translate('почати'), callback_data='почати'))
        keyboard.add(InlineKeyboardButton(text=language.translate('показати налаштування'), callback_data='show settings'))
        keyboard.add(InlineKeyboardButton(text=language.translate('пара'), callback_data='pair'))
        keyboard.add(InlineKeyboardButton(text=language.translate('початок'), callback_data='start'))
        keyboard.add(InlineKeyboardButton(text=language.translate('кінець'),callback_data='end'))
        keyboard.add(InlineKeyboardButton(text=language.translate('інтервал'),callback_data='interval'))
        keyboard.add(InlineKeyboardButton(text=language.translate('відстань'),callback_data='distance'))
        return keyboard