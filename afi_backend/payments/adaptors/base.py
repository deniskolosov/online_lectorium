from builtins import NotImplementedError


class BasePaymentAdaptor:
    def pay(self):
        raise NotImplementedError()
