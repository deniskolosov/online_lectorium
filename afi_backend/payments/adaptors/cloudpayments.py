from django.conf import settings
from django.urls import reverse

import uuid
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
        return settings.SITE_URL + reverse('payments:cloudpayments-payment-form', kwargs={
            'amount':value,
            'description': description,
            'currency': currency,
            'payment_id': internal_payment_id,
        })
