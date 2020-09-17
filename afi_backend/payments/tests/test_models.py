import pytest

from afi_backend.payments.models import Payment, PaymentMethod, create_payment_with_paid_object_and_link
from afi_backend.tickets.models import Ticket
from afi_backend.payments.tests.factories import PaymentMethodFactory
from afi_backend.users.tests.factories import UserFactory
from afi_backend.events.tests.factories import OfflineLectureFactory

pytestmark = pytest.mark.django_db


def test_create_payment_func():
    payment_method = PaymentMethodFactory()
    test_user = UserFactory()
    offline_lecture = OfflineLectureFactory()
    test_payment = create_payment_with_paid_object_and_link(
        payment_type=payment_method.payment_type,
        user=test_user,
        payment_for='ticket',
        related_object_id=offline_lecture.id
    )
    assert test_payment == Payment.objects.first()
    assert test_payment.content_object == Ticket.objects.first()
    assert test_payment.content_object.offline_lecture == offline_lecture
