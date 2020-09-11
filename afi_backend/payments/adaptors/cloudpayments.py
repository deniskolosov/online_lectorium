import uuid

from django.conf import settings
from django.urls import reverse

from afi_backend.payments.adaptors.base import BasePaymentAdaptor


class CloudpaymentsAdaptor(BasePaymentAdaptor):
    """
    Adapter for CloudPayments integration
    """
    def __init__(self):
        """
        Configure cloudpayments here
        """
        pass

    def charge(self, value: str, currency: str, description: str,
               internal_payment_id: uuid.UUID):
        """
        Return link to template view containing Cloudpayments form with all necessary data
        """
        return settings.SITE_URL + reverse(
            'payments:cloudpayments-payment-form',
            kwargs={
                'amount': value,
                'description': description,
                'currency': currency,
                'payment_id': str(internal_payment_id),
            })
