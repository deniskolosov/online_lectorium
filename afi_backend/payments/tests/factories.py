import factory

from afi_backend.cart.models import OrderItem
from afi_backend.cart.tests import factories as cart_factories
from afi_backend.events.tests.factories import VideoLectureFactory
from afi_backend.payments.models import (Payment, PaymentMethod,
                                         VideoLectureOrderItem, Membership, UserMembership, Subscription)
from afi_backend.tickets.tests.factories import TicketFactory
from afi_backend.users.tests.factories import UserFactory
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
    content_object = factory.SubFactory(VideoLectureFactory)

    class Meta:
        model = OrderItem


class VideoLectureOrderItemPaymentFactory(PaymentFactory):
    content_object = factory.SubFactory(VideoLectureOrderItemFactory)

    class Meta:
        model = Payment


class MembershipFactory(factory.django.DjangoModelFactory):
    membership_type = Membership.TIER.PAID
    price = 1000

    class Meta:
        model = Membership


class UserMembershipFactory(factory.django.DjangoModelFactory):
    membership = factory.SubFactory(MembershipFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = UserMembership


class SubscriptionFactory(factory.django.DjangoModelFactory):
    user_membership = factory.SubFactory(UserMembershipFactory)
    payment_method = factory.SubFactory(PaymentMethodFactory)

    class Meta:
        model = Subscription
