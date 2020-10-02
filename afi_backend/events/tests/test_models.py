import pytest
from afi_backend.events.tests.factories import OfflineLectureFactory
from afi_backend.tickets.tests.factories import TicketFactory

pytestmark = pytest.mark.django_db


def test_offline_lecture_is_enough_space():
    from afi_backend.payments.models import Payment
    offline_lecture = OfflineLectureFactory(capacity=10)
    # Create 9 tickets, selling one more is okay
    TicketFactory.create_batch(9,
                               offline_lecture=offline_lecture,
                               is_paid=True)
    assert offline_lecture.is_enough_space
    # create another one, selling more is not allowed
    TicketFactory(offline_lecture=offline_lecture, is_paid=True)
    assert not offline_lecture.is_enough_space
