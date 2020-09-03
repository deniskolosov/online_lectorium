

from .base import BasePaymentAdaptor


class CloudpaymentsAdaptor(BasePaymentAdaptor):
    """
    """
    def __init__(self):
        """
        Configure cloudpayments here
        """
        pass


    def charge(self, value:str, currency:str, description:str, internal_payment_id:uuid.UUID):
        pass
