from django.db import models

from afi_backend.users.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from afi_backend.payments.models import Payable
"""
Buying process:
User clicks the button, sends request to create OrderItem, if cart is not present for user, create it,
add OrderItem to cart. after User finishes adding items, they make request to Payment with 'cart' param and cart id
When payment is made, do_afterpayment_logic is called, where Cart should probably call afterpaymentlogic for all payable items in it's order items. (connect with user for example for video lecture)

"""


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
        self.order_items.update(is_paid=True)
