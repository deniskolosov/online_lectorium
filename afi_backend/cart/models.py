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
    item = models.ForeignKey(ContentType,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)

    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('item', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)


class Cart(Payable):
    """
    Cart which consists of Order Items
    """
    order_items = models.ManyToManyField(OrderItem)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def do_afterpayment_logic(self, customer=None):
        """
        Calls do_afterpayment_logic for each item in the cart.
        """
        for order_item in self.order_items.all():
            order_item.content_object.do_afterpayment_logic(customer=customer)
