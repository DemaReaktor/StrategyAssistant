from enum import IntEnum
from datetime import datetime


class OrderType(IntEnum):
    Buy = 0
    Sell = 1


class OrderStatus(IntEnum):
    Active = 0
    Canceled = 1
    Successfully = 2


class Order:
    """simulation of real order"""
    def __init__(self, type:OrderType, price:float, count:float, start:datetime):
        if not (isinstance(type, OrderType)):
            raise TypeError('type should have type "OrderType"')
        if not (isinstance(price, float)):
            raise TypeError('price should have type "float"')
        if not (isinstance(count, float)):
            raise TypeError('count should have type "float"')
        if not (isinstance(start, datetime)):
            raise TypeError('start should have type "datetime"')
        self.__type = type
        self.__price = price
        self.__status = OrderStatus.Active
        self.__count = count
        self.__start = start
        self.__end = None

    @property
    def start(self)->datetime:
        return self.__start

    @property
    def end(self)->datetime:
        return self.__end

    @property
    def type(self)->OrderType:
        return self.__type

    @property
    def price(self)->float:
        return self.__price

    @property
    def status(self)->OrderStatus:
        return self.__status

    @property
    def count(self)->float:
        return self.__count

    def update(self, price:float, time:datetime):
        """check has order price more than current price if order is buy and over against
        check only active order"""
        if not (isinstance(price, float)):
            raise TypeError('price should have type "float"')
        if not (isinstance(time, datetime)):
            raise TypeError('time should have type "datetime"')
        if not(self.__status == OrderStatus.Active):
            return
        if ((self.__type == OrderType.Buy and price <= self.__price) or
                (self.__type == OrderType.Sell and price >= self.__price)):
            self.__status = OrderStatus.Successfully
            self.__end = time

    def cancel(self):
        """cancel order"""
        self.__status = OrderStatus.Canceled
