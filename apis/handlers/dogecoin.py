import logging
from decimal import Decimal

import requests
from django.conf import settings as app_settings

from apis.handlers import BaseHandler
from utils.handlers import handle_log_request_data


logger = logging.getLogger('request')


class DOGEHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.url = app_settings.GETBLOCK_DOGECOIN_BLOCKBOOK_ADDR
        self.url_test = app_settings.GETBLOCK_DOGECOIN_BLOCKBOOK_ADDR_TEST

    def parsing_balance(self, response):
        log_data = handle_log_request_data(response)
        try:
            resp_json = response.json()
            balance_sts = Decimal(resp_json["balance"])

            logger.info(msg='Success get doge coin balance', extra=log_data)
            return balance_sts / 100000000

        except Exception as e:
            log_data['Exception'] = str(e)
            logger.error(msg='Error get doge coin balance', extra=log_data)
            return

    def get_balance(self, address):
        url = f"{self.url}v2/address/{address}"
        params = {"page": 1, "pageSize": 1, "details": "basic", "secondary": "ltc"}

        response = requests.get(url, params=params)

        return self.parsing_balance(response)

    def get_balance_test(self, address):
        url = f"{self.url_test}v2/address/{address}"
        params = {"page": 1, "pageSize": 1, "details": "basic", "secondary": "ltc"}

        response = requests.get(url, params=params)

        return self.parsing_balance(response)


class DOGEHandlerBlockChair(BaseHandler):
    def __init__(self):
        super().__init__()
        self.url = app_settings.BLOCKCHAIR_DOGECOIN_ADDR
        self.url_test = app_settings.BLOCKCHAIR_DOGECOIN_ADDR_TEST

    def parsing_balance(self, address, response):
        try:
            resp_json = response.json()
            data = resp_json["data"]
            balance_int = data[address]["address"]["balance"]
            balance_dcm = Decimal(balance_int)
            return balance_dcm / 100000000
        except Exception as e:
            print(str(e))
            return

    def get_balance(self, address):
        url = f"{self.url}{address}"
        response = requests.get(url)

        return self.parsing_balance(address, response)

    def get_balance_test(self, address):
        url = f"{self.url_test}{address}"
        response = requests.get(url)

        return self.parsing_balance(address, response)
