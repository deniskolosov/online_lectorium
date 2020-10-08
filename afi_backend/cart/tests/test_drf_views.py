from rest_framework.test import APIClient, force_authenticate

import pytest

from afi_backend.cart.tests.factories import (CartFactory,
                                              OrderItemTicketFactory,
                                              OrderItemVideoLectureFactory)
from afi_backend.users.tests.factories import UserFactory
from afi_backend.events.tests.factories import VideoLectureFactory
from afi_backend.tickets.tests.factories import TicketFactory

pytestmark = pytest.mark.django_db


class TestCartViewSet:
    def test_cart_total_vlecture_and_ticket(self):
        client = APIClient()
        test_user = UserFactory()
        test_cart = CartFactory()
        test_video_lecture = VideoLectureFactory()
        test_ticket = TicketFactory()
        test_video_lecture_oi = OrderItemVideoLectureFactory(
            content_object=test_video_lecture)
        test_ticket_oi = OrderItemTicketFactory(content_object=test_ticket)
        test_cart.order_items.add(test_video_lecture_oi, test_ticket_oi)

        client.force_authenticate(user=test_user)
        response = client.get('/api/cart/')
        assert response.status_code == 200
        cart_total = response.json()['data'][0]['attributes']['total']
        assert cart_total == int(
            (test_ticket.price + test_video_lecture.price).round(1).amount)

    def test_cart_total_vlecture_only(self):
        client = APIClient()
        test_user = UserFactory()
        test_cart = CartFactory()
        test_video_lecture = VideoLectureFactory()
        test_video_lecture_oi = OrderItemVideoLectureFactory(
            content_object=test_video_lecture)
        test_cart.order_items.add(test_video_lecture_oi)

        client.force_authenticate(user=test_user)
        response = client.get('/api/cart/')
        assert response.status_code == 200
        cart_total = response.json()['data'][0]['attributes']['total']
        assert cart_total == int(test_video_lecture.price.round(1).amount)

    def test_buy_one(self):
        client = APIClient()
        test_user = UserFactory()
        test_cart = CartFactory()
        test_video_lecture = VideoLectureFactory()
        client.force_authenticate(user=test_user)
        test_data = {
            "data": {
                "type": "OrderItem",
                "attributes": {
                    "customer_email": test_user.email,
                    "item_type": 'videolecture',
                    "object_id": test_video_lecture.id,
                }
            }
        }
        response = client.post('/api/cart/buy-one/', data=test_data)
        assert response.status_code == 200
        assert test_video_lecture == test_user.order_items.first(
        ).content_object
