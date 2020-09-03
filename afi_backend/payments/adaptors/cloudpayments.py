import uuid

from django.urls import reverse

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
        """
        Return link to template view containing Cloudpayments form with all necessary data
        """
        return reverse('payments:cloudpayments-payment-form', kwargs={
            'amount':int(value),
            'description': description,
            'currency': currency,
        })
