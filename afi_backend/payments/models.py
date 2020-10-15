import logging
from builtins import NotImplementedError
from typing import Union
from django.apps import apps

from django.db import models
from model_utils import Choices, FieldTracker
from model_utils.fields import StatusField

import uuid
from afi_backend.users import models as user_models
from afi_backend.users.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from djmoney.models.fields import MoneyField

logger = logging.getLogger(__name__)


class Payable(models.Model):
    """
    Inherit from this if you want the model to be 'buyable'.
    """
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    is_paid = models.BooleanField(default=False, null=True)

    class Meta:
        abstract = True

    def do_afterpayment_logic(self, *args, **kwargs):
        """
        Logic which should be done after Payment is paid
        """
        raise NotImplementedError()

    @property
    def price(self):
        raise NotImplementedError()


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
        from afi_backend.payments.adaptors import get_adaptor_from_payment_type
        return get_adaptor_from_payment_type(self.payment_type)

    def __str__(self):
        return f"{self.get_payment_type_display()}"


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)

    cart = models.ForeignKey('cart.Cart',
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.CASCADE,
        default=PaymentMethod.TYPE_YANDEX_CHECKOUT)
    external_id = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS = Choices((0, 'PENDING', 'pending'), (1, 'PAID', 'paid'))
    status = models.IntegerField(choices=STATUS, default=STATUS.PENDING)

    tracker = FieldTracker()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # If payment is completed for item, do afterpayment logic
        if self.tracker.has_changed('status') and self.tracker.previous(
                'status') == self.STATUS.PENDING:
            logger.info(f"Saving payment {self.id}")

            self.cart.do_afterpayment_logic(customer=self.user)


def link_payment_with_cart(payment_type: int, user: User,
                           cart_id: int) -> Payment:
    from afi_backend.cart.models import Cart
    # Payment provider(Yandex Checkout, Cloudpayments, etc.)
    payment_method = PaymentMethod.objects.get(payment_type=payment_type)
    cart = Cart.objects.get(id=cart_id)
    payment = Payment.objects.create(user=user,
                                     payment_method=payment_method,
                                     cart=cart)

    return payment


class VideoLectureOrderItem(Payable):
    # VideoLecture which user purchased
    video_lecture = models.ForeignKey('events.VideoLecture',
                                      on_delete=models.CASCADE)

    @property
    def price(self):
        return self.video_lecture.price


class Membership(models.Model):
    TIER = Choices((0, 'FREE', 'free'), (1, 'PAID', 'paid'))
    membership_type = models.IntegerField(choices=TIER, default=TIER.FREE)
    price = MoneyField(max_digits=10,
                       decimal_places=2,
                       null=True,
                       default=1,
                       default_currency='RUB')


class UserMembership(models.Model):
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "membership",)


class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership,
                                        on_delete=models.CASCADE)
    external_id = models.CharField(max_length=256, null=True, blank=True)
    due = models.DateTimeField(null=True, blank=True)
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.CASCADE,
        default=PaymentMethod.TYPE_YANDEX_CHECKOUT)
    is_active = models.BooleanField(default=True)
    is_trial = models.BooleanField(default=True)
