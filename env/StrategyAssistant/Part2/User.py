from Language import LanguageController
from StrategyAssistant.Scripts.BinanceData import BinanceData
from StrategyAssistant.Scripts.PyramidStrategy import PyramidStrategy
from datetime import datetime
from StrategyAssistant.Scripts.Order import OrderStatus, OrderType

class User:
    def __init__(self, id):
        if not isinstance(id, int):
            raise TypeError('id should have type "int"')
        self.__id = id
        self.__language = LanguageController()
        self.strategy_args = {
            'summa':1000,
            'start':datetime.strptime('01-01-2022', '%d-%m-%Y'),
            'end':datetime.strptime('01-01-2023', '%d-%m-%Y'),
            'interval':'1d',
            'pair': 'BTCUSDT',
            'distance': 0.085,
            'difference_capital': 0.02
                              }
        self.variant = None

    @property
    def id(self):
        return self.__id

    @property
    def lang(self):
        return self.__language

    def try_set_settings(self, key, value):
        if not(key in ['pair','start','end','interval','distance','difference_capital','summa']):
            raise ValueError('key should be pair or start or end or interval or distance or difference_capital')
        if key == 'interaval':
            if not(value in BinanceData.intervals()):
                return ('значення інтервалу може бути тільки 1m або 3m або 5m або 15m або 30m або 1h або 2h або 4h або 6h'
                        'або 8h або 12h або 1d або 3d або 1w')
        if key == 'start':
            try:
                date = datetime.strptime(value, ('%H:%M 'if ':' in value else '')+'%d-%m-%Y')
                if date >= self.strategy_args['end']:
                    return f'старт має бути до кінця, кінець зараз: {"{%H:%M %d-%m-%Y}".format(self.strategy_args["end"])}'
                self.strategy_args[key] = date
                return None
            except Exception as e:
                print(e)
                return 'формат старту має бути день-місяць-рік(додатково година:хвилина), наприклад: 01-01-2023 , 05:55 03-03-2023'
        if key == 'end':
            try:
                date = datetime.strptime(value, ('%H:%M 'if ':' in value else '')+'%d-%m-%Y')
                if date < self.strategy_args['start']:
                    return f'кінець має бути після початку, початок зараз: {"{%H:%M %d-%m-%Y}".format(self.strategy_args["start"])}'
                self.strategy_args[key] = date
                return None
            except Exception as e:
                print(e)
                return 'формат кінця має бути день-місяць-рік(додатково година:хвилина), наприклад: 01-01-2023, 05:55 22-11-2023'
        if key in ['distance','difference_capital','summa']:
            try:
                number = float(value)
                if number <= 0:
                    return 'дане значення має бути більше 0'
                if key == 'distance' and number >= 0.2:
                    return 'дане значення має бути менше 0.2'
                if key == 'difference_capital' and number >= 0.25:
                    return 'дане значення має бути менше 0.25'
                self.strategy_args[key] = number
                return None
            except:
                return 'має бути число'
        self.strategy_args[key] = value
        return None

    def show_settings(self):
        data = dict()
        for key in self.strategy_args.keys():
            if isinstance(self.strategy_args[key], datetime):
                data[key] = '{:%H:%M %d-%m-%Y}'.format(self.strategy_args[key])
                continue
            data[key] = self.strategy_args[key]
        data['summa'] = str(self.strategy_args['summa']) + ' $'
        return ', '.join(f'{key}: {value}' for key,value in data.items()).removeprefix(', ').replace('_', ' ')

    def start_strategy(self):
        binance_kwargs = dict()
        strategy_kwargs = dict()
        summa = self.strategy_args['summa']
        for key in self.strategy_args.keys():
            if key in ['pair','start','end','interval']:
                binance_kwargs[key] = self.strategy_args[key]
            else:
                strategy_kwargs[key] = self.strategy_args[key]
        strategy_kwargs.pop('summa')

        # start
        max_down = 0
        binance_data = BinanceData(**binance_kwargs).get_data_frame()
        strategy = PyramidStrategy(float(binance_data.at[0,'open_price']),**strategy_kwargs)
        strategy.start(binance_data.close_time.iloc[0])
        summas = []
        dates = []

        # update
        for i in range(0, len(binance_data)):
            strategy.update(float(binance_data.at[i,'open_price']), binance_data.at[i,'close_time'])
            income = strategy.get_income_with_active(float(binance_data.at[i,'open_price']))
            summas.append(income)
            dates.append(binance_data.at[i,'close_time'])
            max_down = min(max_down, income)

        # is last order income
        summa_price = 0.
        count = 0
        for order in strategy.orders:
            if order.status == OrderStatus.Active and order.type == OrderType.Sell:
                summa_price += order.price
                count += 1
        last_price = float(binance_data.open_price.iloc[-1])
        is_income_last = 0 if count == 0 else (1 if summa_price / count < last_price else -1)

        # finish strategy
        are_sell_active = any(
            order.type == OrderType.Sell and order.status == OrderStatus.Active for order in strategy.orders)
        strategy.finish(float(binance_data.open_price.iloc[-1]),binance_data.close_time.iloc[-1])

        # set text
        text = 'Результат:\n'
        text += f'кількість успішних угод:' + str(len([order for order in strategy.orders if order.type == OrderType.Sell
                    and order.status == OrderStatus.Successfully]) + (1 if is_income_last == 1 else 0) - are_sell_active)
        text += f'\nкількість провальних угод:' + str(1 if is_income_last == -1 else 0)
        text += f'\nмаксимальна просадка: {round(max_down * 100, 2)}'
        income = strategy.get_income()
        text += f'\nприбуток: {round(income * 100, 2)}%'
        text += f'\nзагальний прибуток: {round(income * summa, 2)} $'
        return (text,summas,dates)
