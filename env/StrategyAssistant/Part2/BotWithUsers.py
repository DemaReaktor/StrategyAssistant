from telebot import TeleBot
from User import User

class BotWithUsers(TeleBot):
    def __init__(self,token : str):
        super().__init__(token)
        self.__users = dict()

    def add_user(self, id):
        if not isinstance(id, int):
            raise TypeError('id should have type "int"')
        self.__users[id] = User(id)

    def get_user(self, id):
        if not isinstance(id, int):
            raise TypeError('id should have type "int"')
        return self.__users[id]