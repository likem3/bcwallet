import os
from bcwallet.settings.base import *
from bcwallet.settings.beat import *
from dotenv import load_dotenv


load_dotenv()

env_file_path = os.path.join(BASE_DIR, '.env')

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