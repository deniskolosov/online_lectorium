import pytest

from afi_backend.payments.models import Payment, PaymentMethod, link_payment_with_cart
from afi_backend.tickets.models import Ticket
from afi_backend.payments.tests.factories import PaymentMethodFactory
from afi_backend.users.tests.factories import UserFactory
from afi_backend.events.tests.factories import OfflineLectureFactory
from afi_backend.cart.tests.factories import CartFactory

pytestmark = pytest.mark.django_db


def test_create_payment_for_cart():
    payment_method = PaymentMethodFactory()
    test_user = UserFactory()
    offline_lecture = OfflineLectureFactory()
    test_cart = CartFactory()
    test_payment = link_payment_with_cart(
        payment_type=payment_method.payment_type,
        user=test_user,
        cart_id=test_cart.id)
    assert test_payment == Payment.objects.first()
    assert test_payment.cart == test_cart
