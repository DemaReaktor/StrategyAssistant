from Order import OrderStatus
from Action import Action, ActionType


class StrategyRealizer:
    def __init__(self, strategy, start_price):
        self.__strategy = strategy
        self.__orders = []
        self.__start_price = start_price

    def start(self, price, time):
        action = Action(ActionType.Start, price, time)
        self.__orders = self.__strategy(action, self.__start_price, self.__orders)

    def finish(self, price, time):
        action = Action(ActionType.Finish, price, time)
        self.__orders = self.__strategy(action, self.__start_price, self.__orders)

    def update(self, price, time):
        action = Action(ActionType.Update, price, time)
        [order.update(price, time) for order in self.__orders]
        self.__orders = self.__strategy(action, self.__start_price, self.__orders)

    @property
    def orders(self):
        return self.__orders

    @property
    def active_orders(self):
        return [element for element in self.__orders if element.OrderStatus == OrderStatus.Active]

