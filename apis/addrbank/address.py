import logging
import requests

from apis.addrbank import BaseAddrBank
from utils.handlers import handle_log_request_data

logger = logging.getLogger('request')


class Address(BaseAddrBank):
    _address = None
    _label = None
    _currency = None
    _network = None
    _json = None

    def __init__(self):
        super(Address, self).__init__()

    def get_assign_address(self, merchant_code, currency_id, user_id):
        url = f"{self.base_url}address/"
        data = {
            "currency_id": currency_id,
            "merchant_code": merchant_code,
            "user_id": user_id,
        }
        api_response = requests.post(url=url, data=data)

        log_data = handle_log_request_data(api_response)

        if api_response.status_code not in [200, 201]:
            logger.error(msg='Error request address', extra=log_data)
            return

        logger.info(msg='Success request address', extra=log_data)

        return api_response.json()

    def get_currency_network(self, network={}):
        if network and network.get("type"):
            return network["type"]
        return "mainnet"

    def create_address(self, merchant_code, currency_id, user_id):
        try:
            json_response = self.get_assign_address(merchant_code, currency_id, user_id)

            if not json_response:
                logger.error(msg='create_address json_response empty')
                return

            self._address = json_response["address"]
            self._label = json_response["label"]
            self._currency = json_response["currency"]
            self._network = self.get_currency_network(
                network=self._currency.get("network")
            )
            self._json = {"status": True, "result": json_response}

        except Exception as e:
            self._json = {
                "status": False,
                "result": "generate_deposit_address: %s\n" % str(e),
            }
            logger.error(msg='Error request address', extra=self._json)

    def create_fake_address(self, currency_id, user_id):
        import random
        import string

        def generate_fake_wallet_address():
            alphabet = string.ascii_lowercase + string.digits
            address_length = (
                42  # Crypto wallet addresses are typically 42 characters long
            )

            # Generate a random string of alphanumeric characters
            fake_address = "".join(random.choices(alphabet, k=address_length))

            return fake_address

        json_response = {
            "currency_id": currency_id,
            "user_id": 122,
            "address": generate_fake_wallet_address(),
            "label": f"fake address - {user_id}",
            "currency": {
                "id": 100000,
                "name": "Fake",
                "symbol": "FKE",
                "blockchain": "fakecoin",
                "std": "FKE20",
            },
        }

        self._address = json_response["address"]
        self._label = json_response["label"]
        self._currency = json_response["currency"]
        self._json = {"status": True, "result": json_response}
