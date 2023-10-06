from StrategyAssistant.Scripts.BinanceData import BinanceData
from StrategyAssistant.Scripts.Order import OrderStatus, OrderType
from StrategyAssistant.Scripts.PyramidStrategy import PyramidStrategy
from datetime import datetime

if __name__ == '__main__':
    # get historical info about price
    data_frame = BinanceData(start=datetime.strptime('21-03-2023', '%d-%m-%Y'),
                             end=datetime.strptime('01-10-2023', '%d-%m-%Y'),
                             interval='1d',
                             pair='ETHUSDT'
                             ).get_data_frame()
    # start strategy
    strategy = PyramidStrategy(float(data_frame.open_price.iloc[0]))
    strategy.start(data_frame.at[0, 'close_time'])

    # set historical prices into strategy
    data_frame.close_time = [datetime.fromtimestamp(data_frame.iloc[i].close_time / 1000.0) for i in range(0, len(data_frame))]
    for i in range(0, len(data_frame)):
        strategy.update(float(data_frame.iloc[i].open_price), data_frame.iloc[i].close_time)

    # Do active sell orders have average price more than current price? (Will last sell order be income or not?)
    summa_price = 0.
    count = 0
    for order in strategy.orders:
        if order.status == OrderStatus.Active and order.type == OrderType.Sell:
            summa_price += order.price
            count += 1
    last_price = float(data_frame.open_price.iloc[-1])
    is_income_last = 0 if count == 0 else (1 if summa_price / count > last_price else -1)

    # finish strategy
    strategy.finish(last_price, data_frame.close_time.iloc[-1])

    # get statistics
    print('income orders:' + str(len([order for order in strategy.orders if order.type == OrderType.Sell and
                                  order.status == OrderStatus.Successfully]) + 1 if is_income_last == 1 else 0))
    print(f'not income orders:' + str(1 if is_income_last == -1 else 0))
    print(f'general income: {round(strategy.get_income()*100,2)}%')
