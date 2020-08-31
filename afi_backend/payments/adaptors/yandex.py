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
        Yandex Response:
        {"amount": {"currency": "RUB", "value": 100.0}, "confirmation": {"confirmation_url": "https://money.yandex.ru/api-pages/v2/payment-confirm/epl?orderId=26df3282-000f-5000-a000-178b3151915a", "type": "redirect"}, "created_at": "2020-08-31T16:01:06.296Z", "description": "Change me", "id": "26df3282-000f-5000-a000-178b3151915a", "metadata": {"scid": "1056615"}, "paid": false, "recipient": {"account_id": "623083", "gateway_id": "1603067"}, "refundable": false, "status": "pending", "test": true}
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

        return payment_response["confirmation"]["confirmation_url"]
