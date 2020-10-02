import factory
from afi_backend.tickets.models import Ticket
from afi_backend.events.tests.factories import OfflineLectureFactory


class TicketFactory(factory.django.DjangoModelFactory):
    offline_lecture = factory.SubFactory(OfflineLectureFactory)

    class Meta:
        model = Ticket
