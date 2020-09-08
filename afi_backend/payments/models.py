import logging
from django.db import models
from model_utils import Choices, FieldTracker
from model_utils.fields import StatusField

import uuid
from afi_backend.users import models as user_models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


logger = logging.getLogger(__name__)

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
        choices=PAYMENT_TYPES, default=TYPE_YANDEX_CHECKOUT)

    def get_adaptor(self):
        from .adaptors import ADAPTORS_MAP
        return ADAPTORS_MAP.get(self.payment_type)

    def __str__(self):
        return f"{self.get_payment_type_display()}"


class Payment(models.Model):
    # PAYMENT_STATUSES = (
    #     (PENDING, "Pending"),
    #     (PAID, "Paid"),
    # )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)

    payment_for = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('payment_for', 'object_id')

    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.CASCADE,
        default=PaymentMethod.TYPE_YANDEX_CHECKOUT)
    external_id = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # status = models.PositiveSmallIntegerField(choices=PAYMENT_STATUSES,
    #                                           default=PENDING)
    STATUS = Choices((0, 'PENDING', 'pending'), (1, 'PAID', 'paid'))
    status = models.IntegerField(choices=STATUS, default=STATUS.PENDING)

    tracker = FieldTracker()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # If payment is completed for item, do afterpayment logic
        logger.info(f"Hello test")
        if self.tracker.has_changed('status') and self.tracker.previous(
                'status') == self.STATUS.PENDING:
            logger.info(f"Calling afterpayment logic for {self.content_object}")

            self.content_object.do_afterpayment_logic()
