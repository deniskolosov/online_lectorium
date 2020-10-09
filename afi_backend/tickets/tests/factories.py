import factory
from afi_backend.tickets.models import Ticket
from afi_backend.events.tests.factories import OfflineLectureFactory
from afi_backend.users.tests.factories import UserFactory


class TicketFactory(factory.django.DjangoModelFactory):
    offline_lecture = factory.SubFactory(OfflineLectureFactory)
    customer = factory.SubFactory(UserFactory)

    class Meta:
        model = Ticket
