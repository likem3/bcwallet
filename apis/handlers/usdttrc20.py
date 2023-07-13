from django.conf import settings as app_settings
import requests
from decimal import Decimal
from apis.handlers import BaseHandler

class USDTTRC20Handler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.url = app_settings.TRONGRID_USDT_ADDR
        self.url_test = app_settings.TRONGRID_USDT_ADDR_TEST

    def parsing_balance(self, address, response, contract_address):
        try:
            resp_json = response.json()
            if not resp_json:
                raise Exception("invalid response")
            
            data = resp_json.get('data', [])
            if not data:
                raise Exception(f"{address} is nonactive")

            account_data = data[0]
            trc_objs = account_data.get('trc20', [])
            if not trc_objs:
                raise Exception(f"{address} no trc20 data")

            trc20_obj = {k: v for item in trc_objs for k, v in item.items()}
            balance = trc20_obj.get(contract_address, '0')

            return Decimal(balance)/1000000

        except Exception as e:
            print(str(e))
            return

    def get_balance(self, address):
        url = f"{self.url}accounts/{address}"
        response = requests.get(url)

        return self.parsing_balance(
            address,
            response,
            contract_address=app_settings.USDT_CONTRACT_ADDRESS
        )

    def get_balance_test(self, address):
        url = f"{self.url_test}accounts/{address}"
        response = requests.get(url)

        return self.parsing_balance(
            address,
            response,
            contract_address=app_settings.USDT_CONTRACT_ADDRESS_NILE
        )
