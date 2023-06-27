from bcwallet.settings import CRYPTOAPI_BASE_URL, CRYPTOAPI_API_KEY, CRYPTOAPI_VERSION


class BaseCryptoAPI:
    base_url = None
    api_key = None
    version = None

    def __init__(self):
        self.base_url = CRYPTOAPI_BASE_URL
        self.api_key = CRYPTOAPI_API_KEY
        self.version = CRYPTOAPI_VERSION
