from enum import Enum
from datetime import datetime


class ActionType(Enum):
    Start = 0
    Update = 1
    Finish = 2


class Action:
    def __init__(self, type, price, time=datetime.now()):
        self.__type = type
        self.__time = time
        self.__price = price

    @property
    def type(self):
        return self.__type

    @property
    def time(self):
        return self.__time

    @property
    def price(self):
        return self.__price

