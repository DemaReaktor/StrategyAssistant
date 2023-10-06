import requests
from pandas import DataFrame
from datetime import datetime
import json


class BinanceData:
    start = int(datetime.strptime('01-01-2023', '%d-%m-%Y').timestamp() * 1000)
    end = int(datetime.now().timestamp()*1000)
    interval = '1d'
    pair = 'BTCUSDT'

    def __init__(self, **kwargs):
        self.__pair = kwargs['pair'] if 'pair' in kwargs.keys() else BinanceData.pair
        self.__start = int(kwargs['start'].timestamp()*1000) if 'start' in kwargs.keys() else BinanceData.start
        self.__end = int(kwargs['end'].timestamp()*1000) if 'end' in kwargs.keys() else BinanceData.end
        self.__interval = kwargs['interval'] if 'interval' in kwargs.keys() else BinanceData.interval

    def get_data_frame(self):
        properties = dict()
        properties['symbol'] = self.__pair
        properties['interval'] = self.__interval
        properties['endTime'] = self.__end
        properties['startTime'] = self.__start
        url = ('https://api.binance.com/api/v1/klines?' +
               '&'.join(f'{key}={value}' for key, value in properties.items()).removeprefix('&'))
        data = json.loads(requests.get(url).text)
        data_frame = DataFrame(data)
        data_frame.columns = ['open_time', 'open_price', 'high_price', 'low_price', 'close_price', 'volume',
                      'close_time', 'quote_asset_volume', 'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore']
        return data_frame
