import factory

from afi_backend.cart.models import OrderItem, Cart
from django.contrib.contenttypes.models import ContentType
from afi_backend.tickets.tests.factories import TicketFactory
from afi_backend.events.tests.factories import VideoLectureFactory
from afi_backend.users.tests.factories import UserFactory
from afi_backend.videocourses.tests.factories import VideoCourseFactory


# https://factoryboy.readthedocs.io/en/latest/recipes.html#django-models-with-genericforeignkeys
class OrderItemFactory(factory.django.DjangoModelFactory):
    object_id = factory.SelfAttribute('content_object.id')
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object))
    customer = factory.SubFactory(UserFactory)

    class Meta:
        exclude = ['content_object']
        abstract = True


class OrderItemTicketFactory(OrderItemFactory):
    content_object = factory.SubFactory(TicketFactory)

    class Meta:
        model = OrderItem


class OrderItemVideoLectureFactory(OrderItemFactory):
    content_object = factory.SubFactory(VideoLectureFactory)

    class Meta:
        model = OrderItem


class OrderItemVideoCourseFactory(OrderItemFactory):
    content_object = factory.SubFactory(VideoCourseFactory)

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
