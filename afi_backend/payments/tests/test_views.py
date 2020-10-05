from unittest.mock import ANY

import pytest
from django.test import Client
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIRequestFactory, force_authenticate

import afi_backend.cart.tests.factories as cart_factories
from afi_backend.events.tests.factories import OfflineLectureFactory
from afi_backend.payments.adaptors.yandex import YandexCheckoutAdaptor as adaptor
from afi_backend.payments.api.views import PaymentCreateView, YandexWebhook
from afi_backend.payments.models import Payment, PaymentMethod
from afi_backend.payments.tests.factories import (PaymentMethodFactory,
                                                  PaymentFactory,
                                                  VideoLectureOrderItemFactory,
                                                  OrderItemVideoLectureFactory)
from afi_backend.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestPaymentViewSet:
    def test_create_payment_view(self, mocker):
        payment_method = PaymentMethodFactory(
            payment_type=PaymentMethod.TYPE_YANDEX_CHECKOUT)
        test_user = UserFactory()
        cart = cart_factories.CartFactory()
        test_url = "https://foo.bar"
        mocked_adaptor = mocker.patch.object(adaptor,
                                             'charge',
                                             autospec=True,
                                             return_value=test_url)

        test_payment_type_value = payment_method.payment_type
        test_amount = "100.00"
        test_currency = "RUB"
        factory = APIRequestFactory()
        view = PaymentCreateView.as_view()
        test_data = {
            "data": {
                "type": "PaymentCreateView",
                "attributes": {
                    "payment_type_value": test_payment_type_value,
                    "amount": test_amount,
                    "currency": test_currency,
                    "cart_id": cart.id,
                }
            }
        }

        request = factory.post('/api/payments/', data=test_data)
        force_authenticate(request, test_user)
        response = view(request)
        assert response.data == {"payment_url": test_url}

        payment = Payment.objects.first()

        assert cart == payment.cart

        mocked_adaptor.assert_called_with(ANY,
                                          value=test_amount,
                                          currency=test_currency,
                                          description=f"Payment #{payment.id}",
                                          internal_payment_id=payment.id)

    def test_raises_validation_error(self):
        factory = APIRequestFactory()
        view = PaymentCreateView.as_view()
        test_user = UserFactory()
        test_data = {"data": {"type": "PaymentCreateView", "attributes": {}}}

        request = factory.post('/api/payments/', data=test_data)
        force_authenticate(request, test_user)
        response = view(request)
        assert response.data == [{
            'detail':
            ErrorDetail(string='payment_type_value field is  required',
                        code='invalid'),
            'status':
            '400',
            'source': {
                'pointer': '/data'
            },
            'code':
            'invalid'
        }]

    def test_pay_for_cart(self, mocker):
        payment_method = PaymentMethodFactory(
            payment_type=PaymentMethod.TYPE_YANDEX_CHECKOUT)
        test_user = UserFactory()
        cart = cart_factories.CartFactory()
        test_order_item = OrderItemVideoLectureFactory()
        cart.order_items.add(test_order_item)
        test_url = "https://foo.bar"
        mocked_adaptor = mocker.patch.object(adaptor,
                                             'charge',
                                             autospec=True,
                                             return_value=test_url)
        test_payment_type_value = payment_method.payment_type
        test_payment_for = "cart"
        test_amount = "100.00"
        test_currency = "RUB"
        factory = APIRequestFactory()
        view = PaymentCreateView.as_view()
        test_data = {
            "data": {
                "type": "PaymentCreateView",
                "attributes": {
                    "payment_type_value": test_payment_type_value,
                    "amount": test_amount,
                    "currency": test_currency,
                    "cart_id": cart.id,
                }
            }
        }

        request = factory.post('/api/payments/', data=test_data)
        force_authenticate(request, test_user)
        response = view(request)
        assert response.data == {"payment_url": test_url}

        payment = Payment.objects.first()
        payment_cart = payment.cart

        assert cart == payment_cart

        mocked_adaptor.assert_called_with(ANY,
                                          value=test_amount,
                                          currency=test_currency,
                                          description=f"Payment #{payment.id}",
                                          internal_payment_id=payment.id)


class TestYandexWebhookView:
    def test_cart_payment(self):
        # Add video lecture, ticket to Cart and check all logic is executed.
        factory = APIRequestFactory()
        view = YandexWebhook.as_view()
        test_external_id = '27068194-000f-5000-9000-1a8dcaefa7ee'
        test_order_item_video_lecture = OrderItemVideoLectureFactory()
        test_order_item_ticket = cart_factories.OrderItemTicketFactory()
        cart = cart_factories.CartFactory.create(order_items=(
            test_order_item_video_lecture,
            test_order_item_ticket,
        ))
        payment = PaymentFactory(external_id=test_external_id, cart=cart)
        test_data = {
            'type': 'notification',
            'event': 'payment.succeeded',
            'object': {
                'id': test_external_id,
                'status': 'succeeded',
                'paid': True,
                'amount': {
                    'value': '8888.00',
                    'currency': 'RUB'
                },
                'authorization_details': {
                    'rrn': '629887981691',
                    'auth_code': '980113'
                },
                'captured_at': '2020-09-30T11:37:08.748Z',
                'created_at': '2020-09-30T11:36:52.215Z',
                'description': 'Payment #8404672d-356a-4532-8901-083e411f9a2c',
                'metadata': {
                    'scid': '1056615'
                },
                'payment_method': {
                    'type': 'bank_card',
                    'id': '27068194-000f-5000-9000-1a8dcaefa7ee',
                    'saved': False,
                    'card': {
                        'first6': '555555',
                        'last4': '4444',
                        'expiry_month': '12',
                        'expiry_year': '2022',
                        'card_type': 'MasterCard',
                        'issuer_country': 'US'
                    },
                    'title': 'Bank card *4444'
                },
                'recipient': {
                    'account_id': '623083',
                    'gateway_id': '1603067'
                },
                'refundable': True,
                'refunded_amount': {
                    'value': '0.00',
                    'currency': 'RUB'
                },
                'test': True
            }
        }
        assert payment.status == Payment.STATUS.PENDING
        assert not hasattr(test_order_item_ticket.content_object, 'qrcode')

        request = factory.post('/api/checkout-wh/',
                               data=test_data,
                               format='json')
        response = view(request)
        # assert Payment is paid, do afterpayment logic is called
        payment.refresh_from_db()
        test_order_item_ticket.content_object.refresh_from_db()

        assert payment.status == Payment.STATUS.PAID
        # ticket: assert code is generated, but not generated before Payment is confirmed
        # video lecture: assert video lecture is avalaible for user, but not available before.
        assert test_order_item_ticket.content_object.qrcode
        # TODO: check video lectures as well
