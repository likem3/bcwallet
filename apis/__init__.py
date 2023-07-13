from apis.handlers.bitcoin import BTCHandler
from apis.handlers.ethereum import EthHandler
from apis.handlers.tron import TronHandler
from apis.handlers.dogecoin import DOGEHandler
from apis.handlers.usdttrc20 import USDTTRC20Handler

class Switcher:
    _handler = None
    _handler_dict = {
        'BTC': BTCHandler,
        'ETH': EthHandler,
        'TRX': TronHandler,
        'DOGE': DOGEHandler,
        'USDTTRC20': USDTTRC20Handler,
    }
    
    @classmethod
    def handler(cls, symbol, std=None):
        key = f"{symbol}{std if std else ''}"
        cls._handler = cls._handler_dict.get(key, None)
        return cls._handler
