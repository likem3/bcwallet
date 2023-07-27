import json

from django.conf import settings
from faker import Faker


class Currency:
    currencies = {
        "BTC": {
            "name": "Bitcoin",
            "symbol": "BTC",
            "blockchain": "bitcoin",
            "std": None,
        },
        "DOGE": {
            "id": 2,
            "name": "Dogecoin",
            "symbol": "DOGE",
            "blockchain": "dogecoin",
            "std": None,
        },
        "LTC": {
            "id": 3,
            "name": "Litecoin",
            "symbol": "LTC",
            "blockchain": "litecoin",
            "std": None,
        },
        "ETH": {
            "id": 4,
            "name": "Ethereum",
            "symbol": "ETH",
            "blockchain": "ethereum",
            "std": None,
        },
        "TRX": {
            "id": 5,
            "name": "Tron",
            "symbol": "TRX",
            "blockchain": "tron",
            "std": None,
        },
        "USDTTRC20": {
            "id": 6,
            "name": "Tether USD",
            "symbol": "USDT",
            "blockchain": "tron",
            "std": "TRC20",
        },
    }
    newtworks = {
        "mainnet": {
            "name": "Mainnet",
            "description": "Mainnet network",
            "type": "mainnet",
        },
        "goerli": {"name": "Goerli", "description": "Goerli network", "type": "goerli"},
        "nile": {"name": "Nile", "description": "Nile network", "type": "nile"},
        "testnet": {
            "name": "Testnet",
            "description": "Testnet Network",
            "type": "testnet",
        },
    }
    currencies_response = {}

    def __init__(self):
        self.faker = Faker()
        for idx, key in enumerate(self.currencies):
            if settings.ENVIRONMENT_SETTING == "production":
                currency = self.currencies[key]
                currency["id"] = idx + 1
                currency["network"] = self.newtworks["mainnet"]

                self.currencies_response[key] = currency

            else:
                currency = self.currencies[key]
                currency["id"] = idx + 1

                if key == "ETH":
                    currency["network"] = self.newtworks["goerli"]

                elif key in ["TRX", "USDTTRC20"]:
                    currency["network"] = self.newtworks["nile"]

                else:
                    currency["network"] = self.newtworks["testnet"]

                self.currencies_response[key] = currency

    def get_currency(self, symbol):
        return self.currencies_response.get(symbol, {})

    def get_address(self, symbol, merchant_code, user_id):
        currency = self.currencies_response.get(symbol, {})
        if currency:
            address = {
                "currency_id": currency["id"],
                "user_id": user_id,
                "address": self.faker.sha256(),
                "label": f"{merchant_code} - {currency['symbol']} - {user_id}",
                "currency": self.currencies_response[symbol],
            }
            return address
        return {}

    def get_currencies(self):
        return self.currencies_response

    def generate_json_response(self):
        return json.dumps(
            {
                "success": True,
                "data": [
                    self.currencies_response[key]
                    for key in self.currencies_response.keys()
                ],
            }
        )
