import logging
import requests

from apis.addrbank import BaseAddrBank
from utils.handlers import handle_log_request_data

logger = logging.getLogger('request')


class Currency(BaseAddrBank):
    def __init__(self):
        super(Currency, self).__init__()

    def get_currencies(self):
        url = f"{self.base_url}currencies/"
        try:
            api_response = requests.get(url)

            response_json = api_response.json()

            log_data = handle_log_request_data(api_response)

            if api_response.status_code != 200:
                logger.error(msg='Error request get currency', extra=log_data)
                return
            else:
                logger.info(msg='Success request get currency', extra=log_data)
                return response_json

        except Exception as e:
            logger.error(msg='Error get currency', extra={'exception': str(e)})
            return

    def get_currency_detail(self, currency_id):
        url = f"{self.base_url}currencies/{currency_id}/"
        try:
            api_response = requests.get(url)

            log_data = handle_log_request_data(api_response)

            if api_response.status_code != 200:
                logger.error(msg='Error request get currency detail', extra=log_data)
                return
            else:
                logger.info(msg='Success request get currency detail', extra=log_data)
                return api_response.json()

        except Exception as e:
            logger.error(msg='Error request get currency detail', extra={'exception': str(e)})
            return
