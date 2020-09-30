import factory

from afi_backend.cart.models import OrderItem, Cart
from django.contrib.contenttypes.models import ContentType
from afi_backend.tickets.tests.factories import TicketFactory
from afi_backend.users.tests.factories import UserFactory


class OrderItemFactory(factory.django.DjangoModelFactory):
    object_id = factory.SelfAttribute('content_object.id')
    item = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object))

    class Meta:
        abstract = True
        exclude = ['content_object']


class OrderItemTicketFactory(OrderItemFactory):
    content_object = factory.SubFactory(TicketFactory)

    class Meta:
        model = OrderItem


class CartFactory(factory.django.DjangoModelFactory):
    is_paid = False
    customer = factory.SubFactory(UserFactory)

    class Meta:
        model = Cart

    @factory.post_generation
    def order_items(self, create, extracted, **kwargs):
        # CartFactory.create(order_items=(item1, item2, item3))
        if not create:
            # simple build, do nothing
            return
        if extracted:
            # A list of order items passed,use them
            for order_item in extracted:
                self.order_items.add(order_item)
