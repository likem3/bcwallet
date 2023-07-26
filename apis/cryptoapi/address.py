from cryptoapis import ApiClient, ApiException, Configuration
from cryptoapis.api import generating_api
from cryptoapis.model.generate_deposit_address_rb import \
    GenerateDepositAddressRB
from cryptoapis.model.generate_deposit_address_rb_data import \
    GenerateDepositAddressRBData
from cryptoapis.model.generate_deposit_address_rb_data_item import \
    GenerateDepositAddressRBDataItem

from apis.cryptoapi import BaseCryptoAPI
from bcwallet.settings import CRYPTOAPI_MASTER_WALLET


class CreateAddressHandler(BaseCryptoAPI):
    master_wallet = None
    cryptoapi = None
    _address = None
    _label = None
    _json = None

    def __init__(self):
        super(CreateAddressHandler, self).__init__()
        self.master_wallet = CRYPTOAPI_MASTER_WALLET

    def create_address(self, blockchain, network, label):
        self.cryptoapi = Configuration(
            host=self.base_url,
            api_key={"ApiKey": self.api_key},
        )

        with ApiClient(self.cryptoapi) as api_client:
            api_instance = generating_api.GeneratingApi(api_client=api_client)
            blockchain = blockchain
            network = network
            wallet_id = self.master_wallet
            context = f"ctx-{label}"
            label_ = f"{label}-{blockchain}-{network}"
            generate_deposit_address_rb = GenerateDepositAddressRB(
                context=context,
                data=GenerateDepositAddressRBData(
                    item=GenerateDepositAddressRBDataItem(label=label_)
                ),
            )

            try:
                api_response = api_instance.generate_deposit_address(
                    blockchain=blockchain,
                    network=network,
                    wallet_id=wallet_id,
                    context=context,
                    generate_deposit_address_rb=generate_deposit_address_rb,
                )

                if (
                    api_response
                    and api_response.get("data")
                    and api_response["data"].get("item")
                ):
                    self._address = api_response["data"]["item"]["address"]
                    self._label = api_response["data"]["item"]["label"]

                self._json = {"status": True, "result": api_response}

            except ApiException as e:
                print(f"generate_deposit_address: {e}")

                self._json = {
                    "status": False,
                    "result": "generate_deposit_address: %s\n" % e,
                }

    def create_fake_adress(self, blockchain, network, label):
        import random
        import string
        import time

        def generate_fake_wallet_address():
            alphabet = string.ascii_lowercase + string.digits
            address_length = (
                42  # Crypto wallet addresses are typically 42 characters long
            )

            # Generate a random string of alphanumeric characters
            fake_address = "".join(random.choices(alphabet, k=address_length))

            return fake_address

        api_response = {
            "api_version": "2023-04-25",
            "context": f"ctx-{label}",
            "data": {
                "item": {
                    "address": generate_fake_wallet_address(),
                    "created_timestamp": time.time(),
                    "label": f"{label}-{blockchain}-{network}",
                }
            },
            "request_id": time.time(),
        }

        if (
            api_response
            and api_response.get("data")
            and api_response["data"].get("item")
        ):
            self._address = api_response["data"]["item"]["address"]
            self._label = api_response["data"]["item"]["label"]

        self._json = {"status": True, "result": api_response}
