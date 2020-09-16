import pytest
from unittest.mock import ANY
from django.test import Client
from rest_framework.test import APIRequestFactory, force_authenticate

from afi_backend.payments.adaptors.yandex import YandexCheckoutAdaptor as adaptor
from afi_backend.payments.api.views import PaymentCreateView
from afi_backend.payments.models import PaymentMethod, Payment
from afi_backend.payments.tests.factories import PaymentMethodFactory
from afi_backend.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestPaymentViewSet:
    def test_create_payment_view(self, mocker):
        payment_method = PaymentMethodFactory(
            payment_type=PaymentMethod.TYPE_YANDEX_CHECKOUT)
        test_user = UserFactory()
        test_url = "https://foo.bar"
        mocked_adaptor = mocker.patch.object(adaptor, 'charge', autospec=True, return_value=test_url)

        test_payment_type_value = payment_method.payment_type
        test_payment_for = "ticket"
        test_amount = "100.00"
        test_currency = "RUB"
        factory = APIRequestFactory()
        view = PaymentCreateView.as_view()
        test_data = {
            "data": {
                "type": "PaymentCreateView",
                "attributes": {
                    "payment_type_value": test_payment_type_value,
                    "payment_for": test_payment_for,
                    "amount": test_amount,
                    "currency": test_currency,
                }
            }
        }

        request = factory.post('/api/payments/', data=test_data)
        force_authenticate(request, test_user)
        response = view(request)
        assert response.data == {"payment_url": test_url}

        payment = Payment.objects.first()

        mocked_adaptor.assert_called_with(
            ANY,
            value=test_amount,
            currency=test_currency,
            description=f"Payment #{payment.id}",
            internal_payment_id=payment.id)
