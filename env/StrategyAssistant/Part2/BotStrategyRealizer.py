from StrategyAssistant.Scripts.StrategyRealizer import StrategyRealizer

class BotStrategyRealizer:
    def __init__(self, strategy_realizer):
        if not issubclass(strategy_realizer, StrategyRealizer):
            raise TypeError('strategy_realizer should have subtype "StrategyRealizer"')
        self.__strategy = strategy_type(**kwargs)

