import json

from django.conf import settings
from yandex_checkout import Configuration, Payment

import uuid
from .base import BasePaymentAdaptor


class YandexCheckoutAdaptor(BasePaymentAdaptor):
    def __init__(self):
        Configuration.configure(settings.YANDEX_CHECKOUT_ACCOUNT_ID,
                               settings.YANDEX_CHECKOUT_SECRET_KEY)


    def charge(self, value:str, currency:str, description:str, internal_payment_id:uuid.UUID) -> str:
        """
        Make a payment request to Yandex Checkout.
        """
        payment_response = Payment.create({"amount": {
            "value": value,
            "currency": currency,
        },
                                           "confirmation": {
                                               "type": "redirect",
                                               "return_url": settings.YANDEX_CHECKOUT_RETURN_URL # replace with user's orders page
                                           },
                                           "capture": True,
                                           "description": description
                                           }, str(internal_payment_id))
        payment_response = json.loads(payment_response.json())
        payment = Payment.objects.get(id=internal_payment_id)
        # TODO: exception handling
        payment.external_id = payment_response.get('id')
        payment.save()

        return  payment_response["confirmation"]["confirmation_url"]
