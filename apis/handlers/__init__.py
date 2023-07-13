class BaseHandler:
    url = None
    url_test = None

    def __init__(self):
        pass

    def get_balance(self, address):
        raise NotImplementedError("Subclasses must implement get_balance() method.")
    
    def get_balance_test(self, address):
        raise NotImplementedError("Subclasses must implement get_balance_test() method.")



