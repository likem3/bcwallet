from apis.addrbank import BaseAddrBank
import requests

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
        except:
            return