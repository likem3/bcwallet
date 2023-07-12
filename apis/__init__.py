from apis.getblock.bitcoin import BTCHandler
from apis.getblock.ethereum import EthHandler
from apis.getblock.tron import TronHandler
from apis.getblock.dogecoin import DOGEHandler

class Switcher:
    _handler = None
    _handler_dict = {
        'BTC': BTCHandler,
        'ETH': EthHandler,
        'TRX': TronHandler,
        'DOGE': DOGEHandler,
        'USDTTRC20': TronHandler
    }
    
    @classmethod
    def handler(cls, symbol, std=None):
        key = f"{symbol}{std if std else ''}"
        cls._handler = cls._handler_dict.get(key, None)
        return cls._handler
