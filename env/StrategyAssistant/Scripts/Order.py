from enum import IntEnum


class OrderType(IntEnum):
    Buy = 0
    Sell = 1


class OrderStatus(IntEnum):
    Active = 0
    Canceled = 1
    Successfully = 2


class Order:
    def __init__(self, type, price, count, start):
        self.__type = type
        self.__price = price
        self.__status = OrderStatus.Active
        self.__count = count
        self.__start = start
        self.__end = None

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @property
    def type(self):
        return self.__type

    @property
    def price(self):
        return self.__price

    @property
    def status(self):
        return self.__status

    @property
    def count(self):
        return self.__count

    def update(self, price, time):
        if not(self.__status == OrderStatus.Active):
            return
        if ((self.__type == OrderType.Buy and price <= self.__price) or
                (self.__type == OrderType.Sell and price >= self.__price)):
            self.__status = OrderStatus.Successfully
            self.__end = time

    def cancel(self):
        self.__status = OrderStatus.Canceled
