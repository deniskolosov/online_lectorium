from django.conf import settings
from yandex_checkout import Configuration, Payment

import uuid
from .base import PaymentProviderBase


class YandexPayment(PaymentProviderBase):
    """
    Class based on Payment info from internal Payment model
    """
    # TODO: Think of replacing currency with Currency objects
    def __init__(self, internal_payment_id: uuid.UUID, value:str, currency=str, description):
        self.account_id = settings.YANDEX_CHECKOUT_ACCOUNT_ID
        self.secret_key = settings.YANDEX_CHECKOUT_SECRET_KEY
        self._configure()
        self.internal_payment_id = internal_payment_id
        self.currency = currency
        self.value = value
        self.description = description

    def make_payment(self, value, currency) -> None:
        """
        Make a payment request to Yandex Checkout.
        """
        payment = Payment.create({"amount": {
            "value": self.value,
            "currency": self.currency,
        },
                                  "confirmation": {
                                      "type": "redirect",
                                      "return_url": settings.YANDEX_CHECKOUT_RETURN_URL # replace with user's orders page
                                  },
                                  "capture": True,
                                  "description": self.description
                                  }, self.internal_payment_id)


    def _configure(self):
        Configuration.configure(self.account_id, self.secret_key)
