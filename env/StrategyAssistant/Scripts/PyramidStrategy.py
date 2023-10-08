from StrategyAssistant.Scripts.StrategyRealizer import StrategyRealizer
from StrategyAssistant.Scripts.Order import OrderStatus, Order, OrderType
from StrategyAssistant.Scripts.Action import ActionType


class PyramidStrategy(StrategyRealizer):
    def __init__(self, start_price, distance = 0.085, difference_capital = 0.02):
        self.__distance = distance if distance >= 0 and distance < 0.25 else 0.085
        self.__difference_capital = difference_capital if difference_capital >= 0 and distance < 0.2 else 0.02
        super().__init__(start_price)
        
    def strategy(self, action, orders):
        if action.type == ActionType.Start:
            self.__prices = []
            for x in range(0, 5):
                self.__prices.append(self._start_price * (1 - x * self.__distance))
                orders.append(Order(OrderType.Buy, self.__prices[x], 0.2 + (x - 2) *
                                    self.__difference_capital, action.time))
            self.__prices.insert(0, self._start_price * (1 + self.__distance))
            return orders
        if action.type == ActionType.Update and hasattr(self, '_PyramidStrategy__prices'):
            for order in action.orders:
                index = [i for i in range(0, 6) if PyramidStrategy.price_equal(order.price, self.__prices[i])][0]
                orders.append(Order(1 - order.type, self.__prices[index - 1 + 2 * order.type],
                                    order.count * self.__prices[index - 1 + 2 * order.type] / order.price, action.time))
        if action.type == ActionType.Finish:
            summa = 0.
            for order in orders:
                if order.status == OrderStatus.Active:
                    order.cancel()
                    if order.type == OrderType.Sell:
                        summa += order.count * action.price / order.price
            if summa > 0:
                order = Order(OrderType.Sell, action.price, summa, action.time)
                order.update(action.price, action.time)
                orders.append(order)
        return orders

    @staticmethod
    def find_index(price, prices):
        for i in range(0, 6):
            if PyramidStrategy.price_equal(price, prices[i]):
                return i
        return -1

    @staticmethod
    def price_equal(price1, price2):
        return abs(price1 - price2) < 1e-3
