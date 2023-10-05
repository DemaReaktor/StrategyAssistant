from BinanceData import BinanceData
from PyramidStrategy import PyramidStrategy
from Order import OrderStatus, OrderType
from datetime import datetime

if __name__ == '__main__':
    data_frame = BinanceData(start=datetime.strptime('20-03-2023', '%d-%m-%Y'),
                             end=datetime.strptime('01-04-2023', '%d-%m-%Y')
                             ).get_data_frame()
    strategy = PyramidStrategy(float(data_frame.open_price.iloc[0]))
    for i in range(0, len(data_frame)):
        data_frame.at[i, 'close_time'] = datetime.fromtimestamp(data_frame.iloc[i].close_time / 1000.0)
        strategy.update(float(data_frame.iloc[i].open_price), data_frame.iloc[i].close_time)
    # for order in strategy.orders:
    #     if order.status == OrderStatus.Successfully:
    #         x = [data_frame.iloc[i] for i in range(0, len(data_frame)) if data_frame.iloc[i].close_time == order.end][0]
    #         print(f'{order.start} :{order.type} :{order.status} :{order.price} :{x.open_price}')
    for order in strategy.orders:
        if order.status == OrderStatus.Successfully:
            x = [data_frame.iloc[i] for i in range(0, len(data_frame)) if data_frame.iloc[i].close_time == order.end][0]
            print(f'{order.start} :{order.type} :{order.status} :{order.price} :{x.open_price}')
        else:
            print(f'{order.start} :{order.type} :{order.status} :{order.price} :None')
    print(1+PyramidStrategy.distance * [order.type == OrderType.Sell and order.status == OrderStatus.Successfully
                                           for order in strategy.orders].count(True))
