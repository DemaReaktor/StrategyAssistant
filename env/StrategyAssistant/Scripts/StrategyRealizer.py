from StrategyAssistant.Scripts.Order import OrderStatus, OrderType
from StrategyAssistant.Scripts.Action import Action, ActionType, Order
from abc import ABC, abstractmethod
from datetime import datetime


class StrategyRealizer(ABC):
    """abstract class that realize strategy"""
    def __init__(self, start_price:float):
        if not (isinstance(start_price, float)):
            raise TypeError('start_price should have type "float"')
        self.__orders = []
        self.__start_price = start_price

    @abstractmethod
    def strategy(self, action:Action, orders:list[Order])->list[Order]:
        """strategy of this class"""
        pass

    def start(self, time:datetime):
        """start strategy"""
        if not (isinstance(time, datetime)):
            raise TypeError('time should have type "datetime"')
        action = Action(ActionType.Start, self.__start_price, time)
        self.__orders = self.strategy(action, self.__orders)

    def finish(self, price:float, time:datetime):
        if not (isinstance(time, datetime)):
            raise TypeError('time should have type "datetime"')
        if not (isinstance(price, float)):
            raise TypeError('price should have type "float"')
        action = Action(ActionType.Finish, price, time)
        self.__orders = self.strategy(action, self.__orders)

    def update(self, price:float, time:datetime):
        """set strtegy new price"""
        if not (isinstance(time, datetime)):
            raise TypeError('time should have type "datetime"')
        if not (isinstance(price, float)):
            raise TypeError('price should have type "float"')
        orders = [order for order in self.__orders if order.status == OrderStatus.Active]
        [order.update(price, time) for order in self.__orders]
        orders = [order for order in orders if not (order.status == OrderStatus.Active)]
        action = Action(ActionType.Update, price, time, orders=orders)
        self.__orders = self.strategy(action, self.__orders)

    def get_income(self)->float:
        """return summa of income orders"""
        # sell orders
        summa = sum([order.count for order in self.__orders if order.status == OrderStatus.Successfully and
                     order.type == OrderType.Sell])
        # buy orders
        summa -= sum([order.count for order in self.__orders if order.status == OrderStatus.Successfully and
                      order.type == OrderType.Buy])
        return summa

    def get_income_with_active(self, current_price:float)->float:
        """return summa of imcome orders with summa of active orders"""
        if not (isinstance(current_price, float)):
            raise TypeError('current_price should have type "float"')
        summa = self.get_income()
        # active orders
        summa += sum([order.count * current_price / order.price for order in self.__orders if
                      order.status == OrderStatus.Active and order.type == OrderType.Sell])
        return summa

    @property
    def orders(self)->list[Order]:
        return self.__orders

    @property
    def active_orders(self)->list[Order]:
        """return only active orders"""
        return [element for element in self.__orders if element.OrderStatus == OrderStatus.Active]

    @property
    def _start_price(self)->float:
        return self.__start_price
