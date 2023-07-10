import os
from dotenv import load_dotenv


load_dotenv()

ENVIRONMENT_SETTING = os.getenv('ENVIRONMENT_SETTING')

if ENVIRONMENT_SETTING not in ['local', 'development', 'production']:
    print('please provide correct ENVIRONMENT_SETTING on your/project/dir/.env')

if ENVIRONMENT_SETTING == 'production':
    try:
        from bcwallet.settings.setting_production import *
    except:
        print(f'please provide {ENVIRONMENT_SETTING}.py')

elif ENVIRONMENT_SETTING == 'development':
    try:
        from bcwallet.settings.setting_development import *
    except:
        print(f'please provide {ENVIRONMENT_SETTING}.py')

else:
    try:
        from bcwallet.settings.setting_local import *
    except:
        print(f'please provide {ENVIRONMENT_SETTING}.py')


CRYPTOAPI_BASE_URL = os.getenv('CRYPTOAPI_BASE_URL')
CRYPTOAPI_API_KEY = os.getenv('CRYPTOAPI_API_KEY')
CRYPTOAPI_MASTER_WALLET = os.getenv('CRYPTOAPI_MASTER_WALLET')
CRYPTOAPI_VERSION = os.getenv('CRYPTOAPI_VERSION')

ADDRBANK_BASE_URL = os.getenv('ADDRBANK_BASE_URL')

GETBLOCK_API_KEY = os.getenv('GETBLOCK_API_KEY')

GETBLOCK_ETHEREUM_JRPC_ADDR = f'https://eth.getblock.io/{GETBLOCK_API_KEY}/mainnet/'
GETBLOCK_ETHEREUM_JRPC_ADDR_TEST = f'https://eth.getblock.io/{GETBLOCK_API_KEY}/goerli/'

GETBLOCK_TRON_JRPC_ADDR = f'https://trx.getblock.io/{GETBLOCK_API_KEY}/mainnet/fullnode/jsonrpc'
GETBLOCK_TRON_JRPC_ADDR_TEST = f'https://trx.getblock.io/{GETBLOCK_API_KEY}/testnet/fullnode/jsonrpc'

GETBLOCK_BTC_BLOCKBOOK_ADDR = f'https://btc.getblock.io/{GETBLOCK_API_KEY}/mainnet/blockbook/api/'
GETBLOCK_BTC_BLOCKBOOK_ADDR_TEST = f'https://btc.getblock.io/{GETBLOCK_API_KEY}/testnet/'

BLOCKCHAIN_DOGE_ADDR = 'https://api.blockchair.com/dogecoin/dashboards/address/'
BLOCKCHAIN_DOGE_ADDR_TEST = 'https://api.blockchair.com/dogecoin/dashboards/address/'