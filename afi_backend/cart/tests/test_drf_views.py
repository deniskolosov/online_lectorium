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
    def test_cart_total(self):
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
