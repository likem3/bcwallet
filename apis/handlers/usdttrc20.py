import logging
from decimal import Decimal

import requests
from django.conf import settings as app_settings

from apis.handlers import BaseHandler
from utils.handlers import handle_log_request_data


logger = logging.getLogger('request')


class USDTTRC20Handler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.url = app_settings.TRONGRID_USDT_ADDR
        self.url_test = app_settings.TRONGRID_USDT_ADDR_TEST

    def parsing_balance(self, address, response, contract_address):
        log_data = handle_log_request_data(response)
        try:
            resp_json = response.json()
            if not resp_json:
                raise Exception("invalid response")

            data = resp_json.get("data", [])
            if not data:
                raise Exception(f"{address} is nonactive")

            account_data = data[0]
            trc_objs = account_data.get("trc20", [])
            if not trc_objs:
                raise Exception(f"{address} no trc20 data")

            trc20_obj = {k: v for item in trc_objs for k, v in item.items()}
            balance = trc20_obj.get(contract_address, "0")

            logger.info(msg='Success get usdt trc20 balance', extra=log_data)
            return Decimal(balance) / 1000000

        except Exception as e:
            log_data['Exception'] = str(e)
            logger.error(msg='Error get usdt trc20 balance', extra=log_data)
            return

    def get_balance(self, address):
        url = f"{self.url}accounts/{address}"
        response = requests.get(url)

        return self.parsing_balance(
            address, response, contract_address=app_settings.USDT_CONTRACT_ADDRESS
        )

    def get_balance_test(self, address):
        url = f"{self.url_test}accounts/{address}"
        response = requests.get(url)

        return self.parsing_balance(
            address, response, contract_address=app_settings.USDT_CONTRACT_ADDRESS_NILE
        )
