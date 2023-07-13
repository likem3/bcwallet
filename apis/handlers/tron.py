from django.conf import settings as app_settings
from jsonrpcclient import request
import requests
import base58
import binascii
from apis.handlers import BaseHandler


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
        try:
            json_response = response.json()
            amount_hex = json_response.get("result")

            decimal_value = int(amount_hex, 16)
            eth_value = decimal_value / 10**6

            return eth_value
        except Exception as e:
            print(str(e))
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
