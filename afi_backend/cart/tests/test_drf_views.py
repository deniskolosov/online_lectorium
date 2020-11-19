import pytest
from django.utils import timezone
from freezegun import freeze_time
from rest_framework.test import APIClient, force_authenticate

from afi_backend.cart.tests.factories import (
    CartFactory,
    OrderItemTicketFactory,
    OrderItemVideoLectureFactory,
)
from afi_backend.events.tests.factories import VideoLectureFactory
from afi_backend.packages.tests.factories import (
    VideoCoursePackageFactory,
    VideoLecturePackageFactory,
)
from afi_backend.tickets.tests.factories import TicketFactory
from afi_backend.users.tests.factories import UserFactory
from afi_backend.videocourses.tests.factories import VideoCourseFactory

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

    def test_create_cart(self):
        client = APIClient()
        test_user = UserFactory()
        client.force_authenticate(user=test_user)
        test_order_item = OrderItemVideoLectureFactory()
        test_order_item1 = OrderItemVideoLectureFactory()
        test_data = {"data": {"type": "Cart",
                              "attributes": {"order_items": [{"type": "OrderItem", "id": f"{test_order_item.id}"},
                                                             {"type": "OrderItem", "id": f"{test_order_item1.id}"}],
                                             }
                              }}

        response = client.post('/api/cart/', test_data)
        assert response.status_code == 201
        assert response.json()['data']['relationships']['order_items']['meta']['count'] == 2
        assert response.json()['data']['relationships']['order_items']['data'][0]['id'] == f"{test_order_item.id}"
        assert response.json()['data']['relationships']['order_items']['data'][1]['id'] == f"{test_order_item1.id}"


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

    def test_buy_one_videolecture(self):
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

    def test_buy_one_ticket(self):
        client = APIClient()
        test_user = UserFactory()
        test_cart = CartFactory()
        test_ticket = TicketFactory()
        client.force_authenticate(user=test_user)
        test_data = {
            "data": {
                "type": "OrderItem",
                "attributes": {
                    "customer_email": test_user.email,
                    "item_type": 'ticket',
                    "object_id": test_ticket.id,
                }
            }
        }
        response = client.post('/api/cart/buy-one/', data=test_data)
        assert response.status_code == 200
        assert test_ticket == test_user.order_items.first().content_object

    @freeze_time("2012-01-14")
    def test_buy_videolecture_package(self):
        client = APIClient()
        test_user = UserFactory()
        test_cart = CartFactory()
        test_video_lecture = VideoLectureFactory()
        test_video_lecture1 = VideoLectureFactory()
        test_videolecture_package = VideoLecturePackageFactory()
        test_videolecture_package.videolectures.add(test_video_lecture,
                                                    test_video_lecture1)
        test_videolecture_package.save()
        client.force_authenticate(user=test_user)
        test_data = {
            "data": {
                "type": "OrderItem",
                "attributes": {
                    "customer_email": test_user.email,
                    "item_type": 'videolecturepackage',
                    "object_id": test_videolecture_package.id,
                }
            }
        }
        response = client.post('/api/cart/buy-one/', data=test_data)
        test_user_order_item = test_user.order_items.first()
        assert response.status_code == 200
        assert test_videolecture_package == test_user_order_item.content_object
        test_user.order_items.update(is_paid=True)
        response = client.get(f'/api/users/{test_user.email}/purchased-items/')
        assert response.status_code == 200
        assert response.json()["data"] == [{
            'type': 'OrderItem',
            'id': str(test_user_order_item.id),
            'attributes': {
                'created_at': '2012-01-14T04:00:00+04:00',
                'is_paid': True
            },
            'relationships': {
                'content_object': {
                    'data': [{
                        'allowed_memberships': [],
                        'bullet_points': [],
                        'category': {
                            'type': 'Category',
                            'id': str(test_video_lecture.category.id)
                        },
                        'certificate': {
                            'type': 'VideoLectureCertificate',
                            'id': str(test_video_lecture.certificate.id)
                        },
                        'description':
                        '',
                        'id':
                        test_video_lecture.id,
                        'lecturer': {
                            'type': 'Lecturer',
                            'id': str(test_video_lecture.lecturer.id)
                        },
                        'vimeo_video_id':
                        test_video_lecture.vimeo_video_id,
                        'name':
                        test_video_lecture.name,
                        'picture':
                        test_video_lecture.picture.url,
                        'price':
                        str(test_video_lecture.price.round(2).amount),
                        'price_currency':
                        str(test_video_lecture.price.currency),
                        'tests': [],
                        'type':
                        'VideoLecture'
                    }, {
                        'allowed_memberships': [],
                        'bullet_points': [],
                        'category': {
                            'type': 'Category',
                            'id': str(test_video_lecture1.category.id)
                        },
                        'certificate': {
                            'type': 'VideoLectureCertificate',
                            'id': str(test_video_lecture1.certificate.id)
                        },
                        'description':
                        '',
                        'id':
                        test_video_lecture1.id,
                        'lecturer': {
                            'type': 'Lecturer',
                            'id': str(test_video_lecture1.lecturer.id)
                        },
                        'vimeo_video_id':
                        test_video_lecture1.vimeo_video_id,
                        'name':
                        test_video_lecture1.name,
                        'picture':
                        test_video_lecture1.picture.url,
                        'price':
                        str(test_video_lecture1.price.round(2).amount),
                        'price_currency':
                        str(test_video_lecture1.price.currency),
                        'tests': [],
                        'type':
                        'VideoLecture'
                    }]
                }
            }
        }]

    @freeze_time("2012-01-14")
    def test_buy_videocourse_package(self):
        client = APIClient()
        test_user = UserFactory()
        test_cart = CartFactory()
        now = timezone.now()
        test_video_course = VideoCourseFactory(release_date=now)
        test_video_course1 = VideoCourseFactory(release_date=now)
        test_videocourse_package = VideoCoursePackageFactory()
        test_videocourse_package.videocourses.add(test_video_course,
                                                  test_video_course1)
        test_videocourse_package.save()
        client.force_authenticate(user=test_user)
        test_data = {
            "data": {
                "type": "OrderItem",
                "attributes": {
                    "customer_email": test_user.email,
                    "item_type": 'videocoursepackage',
                    "object_id": test_videocourse_package.id,
                }
            }
        }
        response = client.post('/api/cart/buy-one/', data=test_data)
        test_user_order_item = test_user.order_items.first()
        assert response.status_code == 200
        assert test_videocourse_package == test_user_order_item.content_object
        test_user.order_items.update(is_paid=True)
        response = client.get(f'/api/users/{test_user.email}/purchased-items/')
        assert response.status_code == 200
        assert response.json()['data'] == [{
            'type': 'OrderItem',
            'id': str(test_user_order_item.id),
            'attributes': {
                'created_at': '2012-01-14T04:00:00+04:00',
                'is_paid': True
            },
            'relationships': {
                'content_object': {
                    'data': [{
                        'allowed_memberships': [],
                        'category': {
                            'type': 'Category',
                            'id': str(test_video_course.category.id)
                        },
                        'course_type':
                        None,
                        'course_parts': [],
                        'description':
                        test_video_course.description,
                        'id':
                        test_video_course.id,
                        'is_released':
                        True,
                        'lecturer': {
                            'type': 'Lecturer',
                            'id': f'{test_video_course.lecturer.id}'
                        },
                        'lectures': [],
                        'name':
                        test_video_course.name,
                        'parts': [],
                        'price':
                        str(test_video_course.price.round(2).amount),
                        'price_currency':
                        str(test_video_course.price.currency),
                        'release_date':
                        '2012-01-14T04:00:00+04:00',
                        'type':
                        'VideoCourse'
                    }, {
                        'allowed_memberships': [],
                        'category': {
                            'type': 'Category',
                            'id': str(test_video_course1.category.id)
                        },
                        'course_type':
                        None,
                        'course_parts': [],
                        'description':
                        test_video_course1.description,
                        'id':
                        test_video_course1.id,
                        'is_released':
                        True,
                        'lecturer': {
                            'type': 'Lecturer',
                            'id': f'{test_video_course1.lecturer.id}'
                        },
                        'lectures': [],
                        'name':
                        test_video_course1.name,
                        'parts': [],
                        'price':
                        str(test_video_course1.price.round(2).amount),
                        'price_currency':
                        str(test_video_course1.price.currency),
                        'release_date':
                        '2012-01-14T04:00:00+04:00',
                        'type':
                        'VideoCourse'
                    }]
                }
            }
        }]
