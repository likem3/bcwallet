from django.conf import settings as app_settings


class BaseAddrBank:
    base_url = None

    def __init__(self):
        self.base_url = app_settings.ADDRBANK_BASE_URL
