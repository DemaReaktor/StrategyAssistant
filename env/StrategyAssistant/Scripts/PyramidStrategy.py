from StrategyAssistant.Scripts.StrategyRealizer import StrategyRealizer
from StrategyAssistant.Scripts.Order import OrderStatus, Order, OrderType
from StrategyAssistant.Scripts.Action import ActionType, Action


class PyramidStrategy(StrategyRealizer):
    """strategy realizer with strategy 'Pyramid'"""
    def __init__(self, start_price:float, distance:float = 0.085, difference_capital:float = 0.02):
        """if distance is not in range(0...0.25) It will be have 0.085
        if difference_capital is not in range(0...0.2) It will be have 0.02"""
        if not (isinstance(start_price, float)):
            raise TypeError('start_price should have type "float"')
        if not (isinstance(distance, float)):
            raise TypeError('distance should have type "float"')
        if not (isinstance(difference_capital, float)):
            raise TypeError('difference_capital should have type "float"')
        self.__distance = distance if distance >= 0 and distance < 0.25 else 0.085
        self.__difference_capital = difference_capital if difference_capital >= 0 and distance < 0.2 else 0.02
        super().__init__(start_price)
        
    def strategy(self, action:Action, orders:list[Order]):
        """realized strategy"""
        if not (isinstance(action, Action)):
            raise TypeError('action should have type "Action"')
        if not (isinstance(orders, list)):
            raise TypeError('orders should have type "list"')
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
                index = [i for i in range(0, 6) if PyramidStrategy.__price_equal(order.price, self.__prices[i])][0]
                orders.append(Order((OrderType)(1 - order.type), self.__prices[index - 1 + 2 * order.type],
                                    order.count * self.__prices[index - 1 + 2 * order.type] / order.price, action.time))
        # finish all active orders
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
    def __price_equal(price1:float, price2:float)->float:
        return abs(price1 - price2) < 1e-3
