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