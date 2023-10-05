from Order import OrderStatus


class StrategyRealizer:
    def __init__(self, strategy, start_price):
        self.__strategy = strategy
        self.__orders = []
        self.__start_price = start_price

    def update(self, price, time):
        [order.update(price, time) for order in self.__orders]
        self.__orders = self.__strategy.remove(price, self.__start_price, time, self.__orders)
        self.__orders.extend(self.__strategy.input(price, self.__start_price, time, self.__orders))
        self.__orders.extend(self.__strategy.output(price, self.__start_price, time, self.__orders))

    @property
    def orders(self):
        return self.__orders

    @property
    def active_orders(self):
        return [element for element in self.__orders if element.OrderStatus == OrderStatus.Active]

