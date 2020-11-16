from django.db import models

from afi_backend.users.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from afi_backend.payments.models import Payable


class OrderItem(models.Model):
    """
    Order item contained in the Cart
    """
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True)

    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 related_name='order_items')
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']


class LatestNotPaidCartManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_paid=False).latest('created_at')


class Cart(Payable):
    """
    Cart which consists of Order Items
    """
    order_items = models.ManyToManyField(OrderItem)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    latest_not_paid = LatestNotPaidCartManager()

    def do_afterpayment_logic(self, customer=None):
        """
        Update order items in the cart
        """
        self.is_paid = True
        self.order_items.update(is_paid=True)
        self.save()

    class Meta:
        ordering = ['-created_at']
