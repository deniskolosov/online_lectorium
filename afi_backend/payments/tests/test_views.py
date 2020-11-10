from django.test import Client
import datetime
from django.utils import timezone
from django.test import override_settings
from freezegun import freeze_time
from rest_framework.test import (APIClient, APIRequestFactory,
                                 force_authenticate)
from unittest.mock import ANY
from django.conf import settings
from afi_backend.payments import tasks as payments_tasks

import pytest
from rest_framework.exceptions import ErrorDetail

import afi_backend.cart.tests.factories as cart_factories
from afi_backend.events.tests.factories import OfflineLectureFactory
from afi_backend.payments.adaptors.yandex import YandexCheckoutAdaptor as adaptor
from afi_backend.payments.api.views import PaymentCreateView, YandexWebhook
from afi_backend.payments.models import Membership, Payment, PaymentMethod, Subscription
from afi_backend.payments.tests.factories import (MembershipFactory,
    OrderItemVideoLectureFactory, PaymentFactory, PaymentMethodFactory,
                                                  VideoLectureOrderItemFactory, SubscriptionFactory)
from afi_backend.users.tests.factories import UserFactory
from afi_backend.payments.tests.factories import SubscriptionFactory


pytestmark = pytest.mark.django_db


class TestPaymentViewSet:
    def test_create_payment_view(self, mocker):
        payment_method = PaymentMethodFactory(
            payment_type=PaymentMethod.TYPE_YANDEX_CHECKOUT)
        test_user = UserFactory()
        cart = cart_factories.CartFactory()
        test_url, external_id = ("https://foo.bar", "fff-ooo-bar")
        mocked_adaptor = mocker.patch.object(adaptor,
                                             'charge',
                                             autospec=True,
                                             return_value=(test_url,
                                                           external_id))

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
                                          description=f"Payment #{payment.id}")

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
        test_url, external_id = ("https://foo.bar", "fff-ooo-bar")
        mocked_adaptor = mocker.patch.object(adaptor,
                                             'charge',
                                             autospec=True,
                                             return_value=(test_url,
                                                           external_id))
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
                                          description=f"Payment #{payment.id}")

class TestSubscriptionViewset():
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_charge_user_due_success(self, mocker):
        mocker.patch('afi_backend.payments.tasks.sleep', return_value=None)
        test_payment_method = PaymentMethodFactory()
        test_due = timezone.now()
        test_subscription = SubscriptionFactory(payment_method=test_payment_method, due=test_due)

        test_external_id = '123'
        test_amount = '1000'
        test_currency = 'RUB'
        test_description = 'foobar'

        mocked_adaptor = mocker.patch.object(adaptor,
                                             'charge_recurrent',
                                             autospec=True,
                                             return_value=True)

        payments_tasks.charge_user_due(
            test_payment_method.payment_type,
            test_external_id,
            test_amount,
            test_currency,
            test_description,
            test_subscription.id
        )
        mocked_adaptor.assert_called_with(ANY,
                                          test_external_id,
                                          test_amount,
                                          test_currency,
                                          description=test_description)
        # assert Subscription is updated
        test_subscription.refresh_from_db()
        assert test_subscription.is_active
        assert test_subscription.due
        assert (test_subscription.due - test_due).days == settings.SUBSCRIPTION_LENGTH_DAYS



    def test_create_subscription(self, mocker):
        payment_method = PaymentMethodFactory(
            payment_type=PaymentMethod.TYPE_YANDEX_CHECKOUT)
        test_user = UserFactory()
        test_url, external_id = ("https://foo.bar", "fff-ooo-bar")
        mocked_adaptor = mocker.patch.object(adaptor,
                                             'charge',
                                             autospec=True,
                                             return_value=(test_url,
                                                           external_id))

        test_payment_type_value = payment_method.payment_type
        test_membership_type = Membership.TIER.PAID
        test_membership = MembershipFactory(membership_type=test_membership_type)
        test_amount = "100.00"
        test_currency = "RUB"
        client = APIClient()
        client.force_authenticate(user=test_user)
        test_data = {
            "data": {
                "type": "Subscription",
                "attributes": {
                    "membership_type": test_membership_type,
                    "payment_method": test_payment_type_value,
                }
            }
        }

        response = client.post('/api/payments/subscriptions/get-payment-link/', data=test_data)
        subscription = Subscription.objects.first()
        assert subscription.user_membership.membership == test_membership
        assert response.json() == {'data':
                                   {'type': 'Subscription',
                                    'id': f'{subscription.id}',
                                    'attributes':
                                    {'membership_type': test_membership_type,
                                     'payment_method': test_payment_type_value,
                                     'payment_url': test_url}}}

        mocked_adaptor.assert_called_with(ANY,
                                          value=str(test_membership.price.round(2).amount),
                                          currency=test_currency,
                                          description=f"Subscription #{subscription.id}")



class TestYandexWebhookView:
    def test_cart_payment(self):
        # Add video lecture, ticket to Cart and check all logic is executed.
        factory = APIRequestFactory()
        view = YandexWebhook.as_view()
        test_external_id = '27068194-000f-5000-9000-1a8dcaefa7ee'
        test_user = UserFactory()
        test_order_item_video_lecture = OrderItemVideoLectureFactory(
            customer=test_user)
        test_order_item_ticket = cart_factories.OrderItemTicketFactory(
            customer=test_user)
        test_order_item_videocourse = cart_factories.OrderItemVideoCourseFactory(
            customer=test_user)
        cart = cart_factories.CartFactory.create(order_items=(
            test_order_item_video_lecture,
            test_order_item_ticket,
            test_order_item_videocourse,
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

        assert not test_order_item_ticket.is_paid
        request = factory.post('/api/checkout-wh/',
                               data=test_data,
                               format='json')
        response = view(request)
        # assert Payment is paid, do afterpayment logic is called
        payment.refresh_from_db()
        test_order_item_ticket.refresh_from_db()
        test_order_item_video_lecture.refresh_from_db()
        test_order_item_videocourse.refresh_from_db()

        assert payment.status == Payment.STATUS.PAID
        assert test_order_item_ticket.is_paid
        assert test_order_item_video_lecture.is_paid
        assert test_order_item_videocourse.is_paid
        # ticket: assert code is generated, but not generated before Payment is confirmed
        # video lecture: assert video lecture is avalaible for user, but not available before.
        assert test_order_item_ticket.content_object.qrcode
        assert test_order_item_ticket in test_user.order_items.filter(
            is_paid=True)
        assert test_order_item_video_lecture in test_user.order_items.filter(
            is_paid=True)

        assert test_order_item_videocourse in test_user.order_items.filter(
            is_paid=True)

    def test_subscription_payment_success(self):
        factory = APIRequestFactory()
        view = YandexWebhook.as_view()
        test_external_id = "22e18a2f-000f-5000-a000-1db6312b7767"
        test_checkout_payment_id = "22e18a2f-000f-5000-a000-1db6312b7767"
        subscription = SubscriptionFactory(external_id=test_external_id, is_active=False, is_trial=True)
        test_data = {
            'type': 'notification',
            'event': 'payment.succeeded',
            'object': {
                "id": test_external_id,
                "status": "succeeded",
                "paid": True,
                "amount": {
                    "value": "2.00",
                    "currency": "RUB"
                },
                "authorization_details": {
                    "rrn": "10000000000",
                    "auth_code": "000000"
                },
                "captured_at": "2018-07-18T17:20:50.825Z",
                "created_at": "2018-07-18T17:18:39.345Z",
                "description": "Заказ №72",
                "metadata": {},
                "payment_method": {
                    "type": "bank_card",
                    "id": test_checkout_payment_id,
                    "saved": True,
                    "card": {
                        "first6": "555555",
                        "last4": "4444",
                        "expiry_month": "07",
                        "expiry_year": "2022",
                        "card_type": "MasterCard",
                        "issuer_country": "RU",
                        "issuer_name": "Sberbank"
                    },
                    "title": "Bank card *4444"
                },
                "refundable": True,
                "refunded_amount": {
                    "value": "0.00",
                    "currency": "RUB"
                },
                "recipient": {
                    "account_id": "100001",
                    "gateway_id": "1000001"
                },
                "test": True
            }
        }
        request = factory.post('/api/checkout-wh/',
                               data=test_data,
                               format='json')
        response = view(request)
        assert response.status_code == 200
        assert response.data == {'msg': 'Got it!'}

        subscription.refresh_from_db()

        assert subscription.is_active
        assert not subscription.is_trial
        assert subscription.external_id == test_checkout_payment_id

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_subscription_regular_payment_success(self, mocker):
        # - create subscription
        # - move time forward
        # - mock Yandex Checkout call
        # - run charge subscription task
        # - assert user is charged
        test_external_id = "22e18a2f-000f-5000-a000-1db6312b7767"
        test_checkout_payment_id = "22e18a2f-000f-5000-a000-1db6312b7767"
        test_sub_date = datetime.datetime(2021, 11, 11)
        test_due_date = test_sub_date + timezone.timedelta(days=settings.SUBSCRIPTION_LENGTH_DAYS)
        mocked_adaptor = mocker.patch.object(adaptor,
                                             'charge_recurrent',
                                             autospec=True,
                                             return_value=True)

        with freeze_time(test_sub_date) as frozen_datetime:
            subscription = SubscriptionFactory(external_id=test_external_id, is_active=True,
                                               is_trial=False,
                                               due=test_due_date)
            frozen_datetime.move_to(test_sub_date + timezone.timedelta(days=settings.SUBSCRIPTION_LENGTH_DAYS))
            payments_tasks.charge_user_monthly()
            mocked_adaptor.assert_called_with(ANY,
                                              external_id=test_external_id,
                                              amount=str(subscription.user_membership.membership.price.round(2).amount),
                                              currency=str(subscription.user_membership.membership.price.currency),
                                              description=f"Payment for subsription #{subscription.id}")
            subscription.refresh_from_db()
            assert subscription.is_active
            assert subscription.due > timezone.now() + timezone.timedelta(days=29)




    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_subscription_regular_payment_failure(self, mocker):
        # - create subscription
        # - move time forward
        # - mock Yandex Checkout call
        # - run charge subscription task
        # - return error from Yandex
        # - assert subscription is cancelled
        test_external_id = "22e18a2f-000f-5000-a000-1db6312b7767"
        test_checkout_payment_id = "22e18a2f-000f-5000-a000-1db6312b7767"
        test_sub_date = datetime.datetime(2021, 11, 11)
        test_due_date = test_sub_date + timezone.timedelta(days=settings.SUBSCRIPTION_LENGTH_DAYS)
        # todo: find out why it's not called
        mocked_adaptor = mocker.patch.object(adaptor,
                                             'charge_recurrent',
                                             autospec=True,
                                             return_value=False)

        with freeze_time(test_sub_date) as frozen_datetime:
            subscription = SubscriptionFactory(external_id=test_external_id, is_active=True,
                                               is_trial=False,
                                               due=test_due_date)
            frozen_datetime.move_to(test_sub_date + timezone.timedelta(days=settings.SUBSCRIPTION_LENGTH_DAYS))
            payments_tasks.charge_user_monthly()
            mocked_adaptor.assert_called_with(ANY,
                                              external_id=test_external_id,
                                              amount=str(subscription.user_membership.membership.price.round(2).amount),
                                              currency=str(subscription.user_membership.membership.price.currency),
                                              description=f"Payment for subsription #{subscription.id}")
            subscription.refresh_from_db()
            assert not subscription.is_active
            assert not subscription.due
