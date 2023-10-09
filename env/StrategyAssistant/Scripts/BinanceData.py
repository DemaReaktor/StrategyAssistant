import requests
from pandas import DataFrame
from datetime import datetime
import json

class BinanceData:
    """give information about prices of cryptas"""
    # default values
    __start = int(datetime.strptime('01-01-2023', '%d-%m-%Y').timestamp() * 1000)
    __end = int(datetime.now().timestamp()*1000)
    __interval = '1d'
    __pair = 'BTCUSDT'
    # possible values
    __intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w']

    @classmethod
    def intervals(cls):
        """return all possible values for interval"""
        return BinanceData.__intervals

    def __init__(self, **kwargs):
        """possible keys: pair, start, end, interval
        types of keys: pair and interval: str, start and datetime - datetime
        interval can take only thoose values: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w"""
        for key,value in {'pair':str,'interval':str,'start':datetime,'end':datetime}.items():
            if key in kwargs.keys():
                if not (isinstance(kwargs[key], value)):
                    raise TypeError(f'{key} should have type "{value}"')
        start = int(kwargs['start'].timestamp()*1000) if 'start' in kwargs.keys() else BinanceData.__start
        end = int(kwargs['end'].timestamp() * 1000) if 'end' in kwargs.keys() else BinanceData.__end
        if end <= start:
            raise ValueError('end should be after start')
        if 'interval' in kwargs.keys():
            if not(kwargs['interval'] in BinanceData.__intervals):
                raise ValueError('interval can take only thoose values: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w')
            self.__interval = kwargs['interval']
        else:
            self.__interval = BinanceData.__interval
        self.__pair = kwargs['pair'] if 'pair' in kwargs.keys() else BinanceData.__pair
        self.__start = start
        self.__end = end

    def get_data_frame(self):
        """return DataFrame of prices
        columns: open_time, open_price, high_price, low_price, close_price, volume, close_time, quote_asset_volume,
        num_trades, taker_base_vol, taker_quote_vol, ignore"""
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
