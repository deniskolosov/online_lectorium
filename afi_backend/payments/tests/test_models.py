import pytest

from afi_backend.payments.models import Payment, PaymentMethod, create_payment_with_paid_object
from afi_backend.tickets.models import Ticket
from afi_backend.payments.tests.factories import PaymentMethodFactory
from afi_backend.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_create_payment_func():
    payment_method = PaymentMethodFactory()
    test_user = UserFactory()
    test_payment = create_payment_with_paid_object(
        payment_type=payment_method.payment_type,
        user=test_user,
        payment_for='ticket')
    assert test_payment == Payment.objects.first()
    assert test_payment.content_object == Ticket.objects.first()
