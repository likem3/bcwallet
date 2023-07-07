from django.conf import settings as app_settings
import requests
from decimal import Decimal


class DOGEHandler:
    url = None

    def __init__(self):
        self.url = app_settings.BLOCKCHAIN_DOGE_ADDR

    def parsing_balance(self, address, response):
        try:
            resp_json = response.json()
            data = resp_json['data']
            balance_int = data[address]['address']['balance']
            balance_dcm = Decimal(balance_int)
            return balance_dcm / 100000000
        except Exception as e:
            print(str(e))
            return

    def get_balance(self, address):
        url = f"{self.url}{address}"
        response = requests.get(url)

        return self.parsing_balance(address, response)
