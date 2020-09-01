from django.db import models
import uuid
from afi_backend.users import models as user_models



class PaymentMethod(models.Model):
    TYPE_YANDEX_CHECKOUT = 0
    TYPE_CLOUDPAYMENTS = 1
    TYPE_PAYPAL = 2
    TYPE_ALFA = 3

    PAYMENT_TYPES = (
        (TYPE_YANDEX_CHECKOUT, "Yandex Checkout"),
        (TYPE_CLOUDPAYMENTS, "Cloudpayments"),
        (TYPE_PAYPAL, "PayPal"),
        (TYPE_ALFA, "Alfa-Bank"),
    )


    payment_type = models.PositiveSmallIntegerField(
        choices=PAYMENT_TYPES,
        default=TYPE_YANDEX_CHECKOUT)

    def get_adaptor(self):
        from .adaptors import ADAPTORS_MAP
        return ADAPTORS_MAP.get(self.payment_type)



class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user =  models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, default=PaymentMethod.TYPE_YANDEX_CHECKOUT)