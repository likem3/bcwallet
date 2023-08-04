import logging

import requests
from django.conf import settings as app_settings
from jsonrpcclient import request

from apis.handlers import BaseHandler
from utils.handlers import handle_log_request_data

logger = logging.getLogger('request')


class EthHandler(BaseHandler):
    request_id = None

    def __init__(self):
        super().__init__()
        self.url = app_settings.GETBLOCK_ETHEREUM_JRPC_ADDR
        self.url_test = app_settings.GETBLOCK_ETHEREUM_JRPC_ADDR_TEST
        self.request_id = "getblock.io"

    def parsing_balance(self, response):
        log_data = handle_log_request_data(response)
        try:
            json_response = response.json()
            amount_hex = json_response.get("result")

            decimal_value = int(amount_hex, 16)
            eth_value = decimal_value / 10**18

            logger.info(msg='Success get ethereum balance', extra=log_data)
            return eth_value
        except Exception as e:
            log_data['Exception'] = str(e)
            logger.error(msg='Error get ethereum balance', extra=log_data)
            return

    def get_balance(self, address):
        rpc_response = requests.post(
            self.url,
            json=request(
                method="eth_getBalance", id=self.request_id, params=[address, "latest"]
            ),
        )

        return self.parsing_balance(rpc_response)

    def get_balance_test(self, address):
        rpc_response = requests.post(
            self.url_test,
            json=request(
                method="eth_getBalance", id=self.request_id, params=[address, "latest"]
            ),
        )

        return self.parsing_balance(rpc_response)
