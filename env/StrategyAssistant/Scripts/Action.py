from enum import Enum
from datetime import datetime
from StrategyAssistant.Scripts.Order import Order


class ActionType(Enum):
    Start = 0
    Update = 1
    Finish = 2


class Action:
    """show what and when was happend"""
    def __init__(self, type:ActionType, price:float, time:datetime=datetime.now(), **kwargs):
        if not (isinstance(type, ActionType)):
            raise TypeError('type should have type "ActionType"')
        if not (isinstance(price, float)):
            raise TypeError('price should have type "float"')
        if not (isinstance(time, datetime)):
            raise TypeError('time should have type "datetime"')
        self.__type = type
        self.__time = time
        self.__price = price
        self.__orders = kwargs['orders'] if 'orders' in kwargs.keys() else None

    @property
    def type(self)->ActionType:
        return self.__type

    @property
    def time(self)->datetime:
        return self.__time

    @property
    def orders(self)->list[Order]|None:
        return self.__orders

    @property
    def price(self)->float:
        return self.__price
