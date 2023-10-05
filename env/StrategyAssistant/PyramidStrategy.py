from StrategyRealizer import StrategyRealizer
from Strategy import Strategy
from Order import OrderStatus, Order, OrderType
from Action import ActionType, Action


class PyramidStrategy(StrategyRealizer):
    distance = 0.085
    start_capital_per_cent = 0.16
    difference_capital_per_cent = 0.02

    def __init__(self, start_price):
        super().__init__(Strategy(self.__input, self.__output, self.__remove), start_price)

    @staticmethod
    def __input(action, start_price, orders):
        if action.type == ActionType.Start:
            orders = []
            for x in range(0, 5):
                orders.append(Order(OrderType.Buy, start_price * (1 - x * PyramidStrategy.distance),
                                        PyramidStrategy.start_capital_per_cent + x *
                                    PyramidStrategy.difference_capital_per_cent, action.time))

            return
        new_orders = []
        for x in range(0, 5):
            if not any(PyramidStrategy.price_equal(order.price, start_price * (1. - (x + order.type)
                    * PyramidStrategy.distance)) and order.status == OrderStatus.Active for order in orders):
                this_orders = [order for order in orders if OrderStatus.Successfully and
                    PyramidStrategy.price_equal(order.price, start_price * (1. - (x + order.type) * PyramidStrategy.distance))]
                if len(this_orders) == 0 or this_orders[-1].type == OrderType.Sell:
                    new_orders.append(Order(OrderType.Buy, start_price * (1 - x * PyramidStrategy.distance),
                    PyramidStrategy.start_capital_per_cent + x * PyramidStrategy.difference_capital_per_cent, time))
        return new_orders

    @staticmethod
    def __output(price, start_price, time, orders):
        new_orders = []
        for x in range(0, 5):
            if not any(PyramidStrategy.price_equal(order.price, start_price * (1. + (order.type - x)
                    * PyramidStrategy.distance)) and order.status == OrderStatus.Active for order in orders):
                this_orders = [order for order in orders if OrderStatus.Successfully and
                               PyramidStrategy.price_equal(order.price, start_price * (
                                           1. + (order.type - x) * PyramidStrategy.distance))]
                if len(this_orders) == 0 or this_orders[-1].type == OrderType.Buy:
                    new_orders.append(Order(OrderType.Sell, start_price * (1. - (x + 1) * PyramidStrategy.distance),
                    PyramidStrategy.start_capital_per_cent + (x + 1) * PyramidStrategy.difference_capital_per_cent, time))
        return new_orders

    @staticmethod
    def __remove(action, start_price, orders):
        return orders

    @staticmethod
    def price_equal(price1, price2):
        return abs(price1 - price2) < 1e-3
