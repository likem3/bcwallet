from apis.cryptoapi import BaseCryptoAPI
from bcwallet.settings import CRYPTOAPI_MASTER_WALLET
from cryptoapis import ApiClient, Configuration, ApiException
from cryptoapis.api import informative_api


class ListAddressesHandler(BaseCryptoAPI):
    master_wallet = None
    cryptoapi = None
    _address = None
    _label = None
    _json = None

    def __init__(self):
        super(ListAddressesHandler, self).__init__()
        self.master_wallet = CRYPTOAPI_MASTER_WALLET

    def get_addresses(self, blockchain, network):
        self.cryptoapi = Configuration(
            host=self.base_url,
            api_key={"ApiKey": self.api_key},
        )
        with ApiClient(self.cryptoapi) as api_client:
            blockchain = blockchain
            network = network
            api_instance = informative_api.InformativeApi(api_client=api_client)
            wallet_id = self.master_wallet
            # get_address_balance =
            try:
                k = {"limit": 2, "offset": 1}
                api_response = api_instance.list_deposit_addresses(
                    blockchain=blockchain, network=network, wallet_id=wallet_id, **k
                )
                return api_response
            except ApiException as e:
                print(f"generate_deposit_address: {e}")
                return
