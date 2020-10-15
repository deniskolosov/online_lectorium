from ..models import PaymentMethod
from .alfa_bank import AlfaBankAdaptor
from .cloudpayments import CloudpaymentsAdaptor
from .paypal import PaypalAdaptor
from .yandex import YandexCheckoutAdaptor
from afi_backend.payments.adaptors.base import BasePaymentAdaptor


ADAPTORS_MAP = {
    PaymentMethod.TYPE_YANDEX_CHECKOUT: YandexCheckoutAdaptor(),
    PaymentMethod.TYPE_CLOUDPAYMENTS: CloudpaymentsAdaptor(),
    PaymentMethod.TYPE_PAYPAL: PaypalAdaptor(),
    PaymentMethod.TYPE_ALFA: AlfaBankAdaptor(),
}

def get_adaptor_from_payment_type(payment_type: int) -> BasePaymentAdaptor:
    return ADAPTORS_MAP.get(payment_type)
