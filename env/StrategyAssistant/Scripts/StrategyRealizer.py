from StrategyAssistant.Scripts.Order import OrderStatus, OrderType
from StrategyAssistant.Scripts.Action import Action, ActionType


class StrategyRealizer:
    def __init__(self, strategy, start_price):
        self.__strategy = strategy
        self.__orders = []
        self.__start_price = start_price

    def start(self, time):
        action = Action(ActionType.Start, self.__start_price, time)
        self.__orders = self.__strategy(action, self.__orders)

    def finish(self, price, time):
        action = Action(ActionType.Finish, price, time)
        self.__orders = self.__strategy(action, self.__orders)

    def update(self, price, time):
        orders = [order for order in self.__orders if order.status == OrderStatus.Active]
        [order.update(price, time) for order in self.__orders]
        orders = [order for order in orders if not (order.status == OrderStatus.Active)]
        action = Action(ActionType.Update, price, time, orders=orders)
        self.__orders = self.__strategy(action, self.__orders)

    def get_income(self):
        summa = sum([order.count for order in self.__orders if order.status == OrderStatus.Successfully and
                     order.type == OrderType.Sell])
        summa -= sum([order.count for order in self.__orders if order.status == OrderStatus.Successfully and
                      order.type == OrderType.Buy])
        return summa

    def get_income_with_active(self, current_price):
        summa = self.get_income()
        # summa += sum([order.count for order in self.__orders if order.status == OrderStatus.Active and
        #              order.type == OrderType.Buy])
        summa += sum([order.count * current_price / order.price for order in self.__orders if
                      order.status == OrderStatus.Active and order.type == OrderType.Sell])
        return summa

    @property
    def orders(self):
        return self.__orders

    @property
    def active_orders(self):
        return [element for element in self.__orders if element.OrderStatus == OrderStatus.Active]

    @property
    def _start_price(self):
        return self.__start_price

    @property
    def _strategy(self):
        return self.__strategy
