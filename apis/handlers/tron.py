import binascii
import logging

import base58
import requests
from django.conf import settings as app_settings
from jsonrpcclient import request

from apis.handlers import BaseHandler
from utils.handlers import handle_log_request_data

logger = logging.getLogger('request')


class TronHandler(BaseHandler):
    request_id = None

    def __init__(self):
        super().__init__()
        self.url = app_settings.GETBLOCK_TRON_JRPC_ADDR
        self.url_test = app_settings.GETBLOCK_TRON_JRPC_ADDR_TEST
        self.request_id = "getblock.io"

    def addres_to_hex(self, address):
        decoded = base58.b58decode(address)
        hex_representation = "0x" + binascii.hexlify(decoded[1:-4]).decode()
        return hex_representation

    def parsing_balance(self, response):
        log_data = handle_log_request_data(response)
        try:
            json_response = response.json()
            amount_hex = json_response.get("result")

            decimal_value = int(amount_hex, 16)
            eth_value = decimal_value / 10**6

            logger.info(msg='Success get tron balance', extra=log_data)
            return eth_value

        except Exception as e:
            log_data['Exception'] = str(e)
            logger.error(msg='Error get tron balance', extra=log_data)
            return

    def get_balance(self, address):
        rpc_response = requests.post(
            self.url,
            json=request(
                method="eth_getBalance",
                id=self.request_id,
                params=[self.addres_to_hex(address), "latest"],
            ),
        )

        return self.parsing_balance(rpc_response)

    def get_balance_test(self, address):
        rpc_response = requests.post(
            self.url_test,
            json=request(
                method="eth_getBalance",
                id=self.request_id,
                params=[self.addres_to_hex(address), "latest"],
            ),
        )

        return self.parsing_balance(rpc_response)
