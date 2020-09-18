import pytest
from afi_backend.payments.tests.factories import TicketPaymentFactory
from afi_backend.events.tests.factories import OfflineLectureFactory
from afi_backend.tickets.tests.factories import TicketFactory

pytestmark = pytest.mark.django_db


def test_offline_lecture_is_enough_space():
    from afi_backend.payments.models import Payment
    offline_lecture = OfflineLectureFactory(capacity=10)
    # Create 9 tickets, selling one more is okay
    TicketPaymentFactory.create_batch(
        9,
        status=Payment.STATUS.PAID,
        content_object=TicketFactory(offline_lecture=offline_lecture))
    assert offline_lecture.is_enough_space
    # create another one, selling more is not allowed
    TicketPaymentFactory(status=Payment.STATUS.PAID, content_object=TicketFactory(offline_lecture=offline_lecture))
    assert not offline_lecture.is_enough_space
