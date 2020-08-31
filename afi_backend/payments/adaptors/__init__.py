from ..models import PaymentMethod
from .yandex import YandexCheckoutAdaptor
from .paypal import PaypalAdaptor
from .cloudpayments import CloudpaymentsAdaptor
from .alfa_bank import AlfaBankAdaptor


ADAPTORS_MAP = {
    PaymentMethod.TYPE_YANDEX_CHECKOUT: YandexCheckoutAdaptor(),
    PaymentMethod.TYPE_CLOUDPAYMENTS: CloudpaymentsAdaptor(),
    PaymentMethod.TYPE_PAYPAL: PaypalAdaptor(),
    PaymentMethod.TYPE_ALFA: AlfaBankAdaptor(),
}
