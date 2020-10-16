from builtins import NotImplementedError

class AdaptorException(Exception):
    pass

class BasePaymentAdaptor:
    def pay(self):
        raise NotImplementedError()
