import requests

from apis.addrbank import BaseAddrBank


class Currency(BaseAddrBank):
    def __init__(self):
        super(Currency, self).__init__()

    def get_currencies(self):
        url = f"{self.base_url}currencies/"
        try:
            api_response = requests.get(url)
            if api_response.status_code != 200:
                return
            else:
                return api_response.json()
        except Exception as e:
            print(str(e))
            return

    def get_currency_detail(self, id):
        url = f"{self.base_url}currencies/{id}/"
        try:
            api_response = requests.get(url)
            if api_response.status_code != 200:
                return
            else:
                return api_response.json()
        except Exception as e:
            print(str(e))
            return
