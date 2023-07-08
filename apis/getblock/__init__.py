class BaseHandler:
    url = None

    def __init__(self):
        pass

    def get_balance(self, address):
        raise NotImplementedError("Subclasses must implement get_a() method.")



