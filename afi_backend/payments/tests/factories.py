import factory

from afi_backend.cart.tests import factories as cart_factories
from afi_backend.events.tests.factories import VideoLectureFactory
from afi_backend.payments.models import (Payment, PaymentMethod,
                                         VideoLectureOrderItem)
from afi_backend.tickets.tests.factories import TicketFactory
from afi_backend.users.tests.factories import UserFactory
from afi_backend.cart.models import OrderItem
from django.contrib.contenttypes.models import ContentType


class PaymentMethodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentMethod


# https://factoryboy.readthedocs.io/en/latest/recipes.html#django-models-with-genericforeignkeys
class PaymentFactory(factory.django.DjangoModelFactory):
    payment_method = factory.SubFactory(PaymentMethodFactory)
    user = factory.SubFactory(UserFactory)
    cart = factory.SubFactory(cart_factories.CartFactory)

    class Meta:
        model = Payment


class VideoLectureOrderItemFactory(factory.django.DjangoModelFactory):
    # Payable
    video_lecture = factory.SubFactory(VideoLectureFactory)

    class Meta:
        model = VideoLectureOrderItem


class OrderItemVideoLectureFactory(cart_factories.OrderItemFactory):
    # Order item with content type video lecture (order item)
    content_object = factory.SubFactory(VideoLectureOrderItemFactory)

    class Meta:
        model = OrderItem


class VideoLectureOrderItemPaymentFactory(PaymentFactory):
    content_object = factory.SubFactory(VideoLectureOrderItemFactory)

    class Meta:
        model = Payment
