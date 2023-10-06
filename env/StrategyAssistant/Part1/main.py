import sys
from StrategyAssistant.Scripts.BinanceData import BinanceData
from StrategyAssistant.Scripts.Order import OrderStatus, OrderType
from StrategyAssistant.Scripts.PyramidStrategy import PyramidStrategy
from datetime import datetime
import re

def get_args(args):
    request_args = dict()
    if '--pair' in args:
        request_args['pair'] = args[args.index('--pair') + 1]
    if '--interval' in args:
        request_args['interval'] = args[args.index('--interval') + 1]
    try:
        request_args['start'] = datetime.strptime(args[args.index('--start') + 1], '%d-%m-%Y')
    except:
        request_args['start'] = datetime.strptime('19-03-2023', '%d-%m-%Y')
    try:
        request_args['end'] = datetime.strptime(args[args.index('--end') + 1], '%d-%m-%Y')
    except:
        request_args['end'] = datetime.strptime('01-10-2023', '%d-%m-%Y')

    strategy_args = dict()
    try:
        arg = float(args[args.index('--distance') + 1])
        if arg >= 0 and arg < 0.2:
            strategy_args['distance'] = arg
    except:
        pass
    try:
        arg = float(args[args.index('--difference_capital_per_cent') + 1])
        if arg >= 0 and arg < 0.2:
            strategy_args['difference_capital_per_cent'] = arg
    except:
        pass
    return (request_args, strategy_args)

if __name__ == '__main__':
    args = sys.argv[1:]
    (request_args, strategy_args) = get_args(args)
    # get historical info about price
    try:
        data_frame = BinanceData(**request_args).get_data_frame()
    except:
        print('Error: arguments are invalid')
        exit()

    # start strategy
    strategy = PyramidStrategy(float(data_frame.open_price.iloc[0]),**strategy_args)
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
    is_income_last = 0 if count == 0 else (1 if summa_price / count < last_price else -1)

    # finish strategy
    are_sell_active = any(order.type == OrderType.Sell and order.status == OrderStatus.Active for order in strategy.orders)
    strategy.finish(last_price, data_frame.close_time.iloc[-1])

    print(data_frame.open_price.iloc[-1])
    # get statistics
    print('income orders:' + str(len([order for order in strategy.orders if order.type == OrderType.Sell and
                                  order.status == OrderStatus.Successfully]) + (1 if is_income_last == 1 else 0) -
                                 are_sell_active))
    print(f'not income orders:' + str(1 if is_income_last == -1 else 0))
    print(f'general income: {round(strategy.get_income()*100,2)}%')