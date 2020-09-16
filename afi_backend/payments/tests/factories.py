import factory
from django.contrib.contenttypes.models import ContentType

from afi_backend.payments.models import Payment, PaymentMethod
from afi_backend.users.tests.factories import UserFactory
from afi_backend.tickets.tests.factories import TicketFactory


class PaymentMethodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentMethod


# https://factoryboy.readthedocs.io/en/latest/recipes.html#django-models-with-genericforeignkeys
class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment
        exclude = ['content_object']

    payment_method = factory.SubFactory(PaymentMethodFactory)
    user = factory.SubFactory(UserFactory)
    object_id = factory.SelfAttribute('content_object.id')
    payment_for = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object))


class TicketPaymentFactory(PaymentFactory):
    content_object = factory.SubFactory(TicketFactory)

    class Meta:
        model = Payment
