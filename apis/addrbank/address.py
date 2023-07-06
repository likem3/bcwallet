from apis.addrbank import BaseAddrBank
import requests


class Address(BaseAddrBank):
    _address = None
    _label = None
    _json = None

    def __init__(self):
        super(Address, self).__init__()

    def get_assign_address(self, currency_id, user_id):
        url = f"{self.base_url}address/"
        data = {
            'currency_id': currency_id,
            'user_id': user_id
        }
        api_response = requests.post(url=url, data=data)
        if api_response.status_code not in [200, 201]:
            return
        
        return api_response.json()       

    def create_address(self, currency_id, user_id):
        try:
            json_response = self.get_assign_address(currency_id, user_id)

            if not json_response:
                return

            self._address = json_response['address']
            self._label = json_response['label']
            self._json = {"status": True, "result": json_response}


        except Exception as e:
            print(str(e))
            self._json = {
                "status": False,
                "result": "generate_deposit_address: %s\n" % str(e),
            }

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
            'currency_id': currency_id,
            'user_id': 122,
            'address': generate_fake_wallet_address(),
            'label': f"fake address - {user_id}",
            'currency': {
                "id": 100000,
                "name": "Fake",
                "symbol": "FKE",
                "blockchain": "fakecoin",
                "std": 'FKE20'
            }
        }

        self._address = json_response['address']
        self._label = json_response['label']
        self._json = {"status": True, "result": json_response}