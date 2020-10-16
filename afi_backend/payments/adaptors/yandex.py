import json
import logging
from decimal import Decimal

from django.conf import settings
from yandex_checkout import Configuration, Payment
from yandex_checkout.client import UnauthorizedError

import uuid
from .. import models as payments_models
from .base import BasePaymentAdaptor, AdaptorException

logger = logging.getLogger(__name__)

class YandexPaymentError(AdaptorException):
    pass


class YandexCheckoutAdaptor(BasePaymentAdaptor):
    def __init__(self):
        Configuration.configure(settings.YANDEX_CHECKOUT_ACCOUNT_ID,
                                settings.YANDEX_CHECKOUT_SECRET_KEY)

    def charge(self,
               value: str,
               currency: str,
               description: str,
               save_payment_method: bool = None) -> [str, str]:
        """
        Make a payment request to Yandex Checkout.
        """
        # todo: correct error handling
        try:
            payment_response = Payment.create({
                "amount": {
                    "value": value,
                    "currency": currency,
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": settings.
                    YANDEX_CHECKOUT_RETURN_URL  # replace with user's orders page
                },
                "capture":
                True,
                "description":
                description,
                "save_payment_method":
                save_payment_method
            })
        except UnauthorizedError:
            raise UnauthorizedError("Set Yandex Checkout keys in env vars.")

        payment_response = json.loads(payment_response.json())

        # TODO: exception handling

        return (payment_response["confirmation"]["confirmation_url"],
                payment_response.get('id'))

    def charge_recurrent(self,
                         external_id: str,
                         amount: Decimal,
                         currency: str,
                         description: str) -> bool:
        """
        Charge customer with saved payment information. Return false if not succeeded.
        """
        payment_response = Payment.create({
            "amount": {
                "value": str(amount),
                "currency": currency
            },
            "payment_method_id": external_id,
            "description": description
        })
        payment_response = json.loads(payment_response.json())
        status = payment_response.get('status')
        if status == 'succeeded':
            return True
        if status == 'canceled' and payment_response['cancellation_details']['reason'] == 'permission_revoked':
            return False
        # Raise exception to retry task with backoff.
        raise YandexPaymentError(f"Yandex payment error response {payment_response}")
