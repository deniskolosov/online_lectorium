from .base import BasePaymentAdaptor
from yandex_checkout import Configuration, Payment
from django.conf import settings
import uuid


class YandexCheckoutAdaptor(BasePaymentAdaptor):
    def __init__(self):
        Configuraton.configure(settings.YANDEX_CHECKOUT_ACCOUNT_ID,
                               settings.YANDEX_CHECKOUT_SECRET_KEY)

    def charge(self, value:str, currency:str, description:str, internal_payment_id:uuid.UUID) -> str:
        """
        Make a payment request to Yandex Checkout.
        """
        payment = Payment.create({"amount": {
            "value": value,
            "currency": currency,
        },
                                  "confirmation": {
                                      "type": "redirect",
                                      "return_url": settings.YANDEX_CHECKOUT_RETURN_URL # replace with user's orders page
                                  },
                                  "capture": True,
                                  "description": description
                                  }, internal_payment_id)
