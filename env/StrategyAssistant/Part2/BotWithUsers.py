from telebot.async_telebot import AsyncTeleBot
from User import User

class BotWithUsers(AsyncTeleBot):
    """bot with users data"""
    def __init__(self,token : str):
        super().__init__(token)
        self.__users = dict()

    def add_user(self, id:int):
        if not isinstance(id, int):
            raise TypeError('id should have type "int"')
        self.__users[id] = User(id)

    def get_user(self, id:int)->User:
        if not isinstance(id, int):
            raise TypeError('id should have type "int"')
        return self.__users[id]
