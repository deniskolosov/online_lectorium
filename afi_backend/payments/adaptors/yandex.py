import json
import logging

from django.conf import settings
from yandex_checkout import Configuration, Payment
from yandex_checkout.client import UnauthorizedError

import uuid
from .. import models as payments_models
from .base import BasePaymentAdaptor

logger = logging.getLogger(__name__)


class YandexCheckoutAdaptor(BasePaymentAdaptor):
    def __init__(self):
        Configuration.configure(settings.YANDEX_CHECKOUT_ACCOUNT_ID,
                                settings.YANDEX_CHECKOUT_SECRET_KEY)

    def charge(self, value: str, currency: str, description: str,
               internal_payment_id: uuid.UUID) -> str:
        """
        Make a payment request to Yandex Checkout.
        """
        # todo: correct error handling
        try:
            payment_response = Payment.create(
                {
                    "amount": {
                        "value": value,
                        "currency": currency,
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": settings.
                        YANDEX_CHECKOUT_RETURN_URL  # replace with user's orders page
                    },
                    "capture": True,
                    "description": description
                },
                str(internal_payment_id))
        except UnauthorizedError:
            raise UnauthorizedError("Set Yandex Checkout keys in env vars.")

        payment_response = json.loads(payment_response.json())
        payment = payments_models.Payment.objects.get(id=internal_payment_id)

        # TODO: exception handling
        payment.external_id = payment_response.get('id')
        payment.save()

        return payment_response["confirmation"]["confirmation_url"]
