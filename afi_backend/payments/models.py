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

    def __str__(self):
        return f"{self.get_payment_type_display()}"



class Payment(models.Model):
    PENDING = 0
    PAID = 1

    PAYMENT_STATUSES = (
        (PENDING, "Pending"),
        (PAID, "Paid"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user =  models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, default=PaymentMethod.TYPE_YANDEX_CHECKOUT)
    external_id = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(
        choices=PAYMENT_STATUSES,
        default=PENDING)
