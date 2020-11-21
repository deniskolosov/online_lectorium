import datetime
from freezegun import freeze_time
import io
from django.contrib.auth.tokens import default_token_generator
from django.test import RequestFactory, modify_settings
from rest_framework.test import APIClient, force_authenticate
from typing import BinaryIO, Dict

import pytest
from PIL import Image

from afi_backend.cart.tests.factories import (OrderItemTicketFactory,
                                              OrderItemVideoLectureFactory,
                                              OrderItemVideoCourseFactory)
from afi_backend.events.tests.factories import VideoLectureFactory, OfflineLectureFactory
from afi_backend.payments.tests.factories import OrderItemVideoLectureFactory
from afi_backend.tickets.tests.factories import TicketFactory
from afi_backend.users.api.views import UserViewSet
from afi_backend.users.models import User
from afi_backend.users.tests.factories import UserFactory
from django.utils import timezone

pytestmark = pytest.mark.django_db


class TestUserViewSet:
    client = APIClient()
    test_email = 'test@test.com'
    test_password = '123456'
    test_data = {
        "data": {
            "type": "User",
            "attributes": {
                "email": test_email,
                "password": test_password,
            }
        }
    }

    def test_get_queryset(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request
        view.action = 'list'

        assert user in view.get_queryset()

    def test_me(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user
        test_bdate = datetime.date(2010, 10, 10)
        user.birthdate = test_bdate
        email = user.email

        view.request = request

        view.action = 'get'
        view.format_kwarg = None

        response = view.me(request)

        assert response.data == {
            "email": email,
            "url": f"http://testserver/api/users/{email}",
            "birthdate": test_bdate.strftime("%Y-%m-%d"),
            "userpic": None,
            "name": user.name,
        }

    def test_user_activation_view(self, mocker):
        # create test user
        # generate activation token
        # send uid + token using activation link
        test_user = UserFactory()
        test_token = default_token_generator.make_token(test_user)

        resp = self.client.get(
            f'/api/users/activation/{test_user.id}/{test_token}/')
        assert resp.status_code == 204
        test_user.refresh_from_db()
        assert test_user.is_active

    def _generate_photo_file(self) -> BinaryIO:
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def _post_create_user(self) -> Dict:
        response = self.client.post('/api/users/', self.test_data)
        return response.data

    def test_create_user_upload_picture(self):
        user_data = self._post_create_user()
        assert self.test_email == user_data['email']
        assert f'http://testserver/api/users/{self.test_email}' == user_data[
            'url']
        user = User.objects.get(email=user_data['email'])
        assert user.email == self.test_email

    def test_edit_user_data(self):
        test_user = UserFactory()
        new_name = "Ivan Ivanov"
        new_birthdate = "2020-10-14"
        data = {
            "data": {
                "type": "User",
                "id": test_user.email,
                "attributes": {
                    "name": new_name,
                    "email": test_user.email,
                    "birthdate": new_birthdate,
                }
            }
        }
        self.client.force_authenticate(user=test_user)
        resp = self.client.put(f'/api/users/{test_user.email}/', data=data)
        assert resp.status_code == 200
        assert resp.data["birthdate"] == new_birthdate
        assert resp.data["name"] == new_name

    @freeze_time("2012-01-14")
    def test_user_purchased_items_endpoint(self):
        test_user = UserFactory()
        test_vl_oi = OrderItemVideoLectureFactory(customer=test_user,
                                                  is_paid=True)
        test_ticket_oi = OrderItemTicketFactory(customer=test_user,
                                                is_paid=True)
        test_vl = test_vl_oi.content_object
        test_ticket = test_ticket_oi.content_object
        test_ticket.offline_lecture.lecture_date = timezone.now()
        test_ticket.offline_lecture.save()
        test_data = [{
            'type': 'OrderItem',
            'id': str(test_vl_oi.id),
            'attributes': {
                'created_at': '2012-01-14T04:00:00+04:00',
                'is_paid': True
            },
            'relationships': {
                'content_object': {
                    'data': {
                        'id': test_vl.id,
                        'vimeo_video_id': test_vl.vimeo_video_id,
                        'certificate': {
                            'type': 'VideoLectureCertificate',
                            'id': str(test_vl.certificate.id)
                        },
                        'name': test_vl.name,
                        'picture': test_vl.picture.url,
                        'lecturer': {
                            'name': test_vl.lecturer.name,
                            'userpic': None,
                            'bio': test_vl.lecturer.bio,
                        },
                        'category': {
                            'type': 'Category',
                            'id': str(test_vl.category.id)
                        },
                        'description': '',
                        'price': str(test_vl.price.round(2).amount),
                        'price_currency': 'RUB',
                        'bullet_points': [],
                        'allowed_memberships': [],
                        'tests': [],
                        'type': 'VideoLecture',
                    }
                }
            }
        }, {
            'type': 'OrderItem',
            'id': str(test_ticket_oi.id),
            'attributes': {
                'created_at': '2012-01-14T04:00:00+04:00',
                'is_paid': True
            },
            'relationships': {
                'content_object': {
                    'data': {
                        'id': str(test_ticket.id),
                        'customer_email': test_ticket.customer.email,
                        'activation_link':
                        f'https://afi-backend.herokuapp.com/api/tickets/activate/{test_ticket.qrcode.code}',
                        'scanned': test_ticket.scanned,
                        'offline_lecture_id':
                        str(test_ticket.offline_lecture.id),
                        'offline_lecture': {
                            'name':
                            test_ticket.offline_lecture.name,
                            'address':
                            test_ticket.offline_lecture.address,
                            'picture':
                            test_ticket.offline_lecture.picture.url,
                            'lecture_date':
                            '2012-01-14T04:00:00+04:00',
                            'lecture_date_ts':
                            test_ticket.offline_lecture.lecture_date_ts(),
                            'lecturer': {
                                'type': 'Lecturer',
                                'id':
                                f'{test_ticket.offline_lecture.lecturer.id}',
                            },
                            'category': {
                                'type': 'Category',
                                'id':
                                f'{test_ticket.offline_lecture.category.id}'
                            },
                            'capacity':
                            None,
                            'description':
                            '',
                            'tickets_sold':
                            0,
                            'lecture_summary_file':
                            None,
                            'price':
                            '1000.00',
                            'price_currency':
                            'RUB'
                        },
                        'type': 'Ticket'
                    }
                }
            }
        }]
        self.client.force_authenticate(user=test_user)
        resp = self.client.get(
            f'/api/users/{test_user.email}/purchased-items/')
        assert resp.status_code == 200
        assert test_data == resp.json()['data']

    def test_purchased_items_filter(self):
        test_user = UserFactory()
        test_vl_oi = OrderItemVideoLectureFactory(customer=test_user,
                                                  is_paid=True)
        test_ticket_oi = OrderItemTicketFactory(customer=test_user,
                                                is_paid=True)
        test_vl = test_vl_oi.content_object
        test_ticket = test_ticket_oi.content_object
        test_videocourse_oi = OrderItemVideoCourseFactory(customer=test_user,
                                                          is_paid=True)
        test_videocourse = test_videocourse_oi.content_object

        self.client.force_authenticate(user=test_user)
        resp = self.client.get(
            f'/api/users/{test_user.email}/purchased-items/?filter[item_type]=videolecture'
        )
        assert resp.status_code == 200
        data = resp.json()['data']
        assert len(data) == 1
        assert data[0]['relationships']['content_object']['data'][
            'type'] == 'VideoLecture'

        resp = self.client.get(
            f'/api/users/{test_user.email}/purchased-items/?filter[item_type]=ticket'
        )
        assert resp.status_code == 200
        data = resp.json()['data']
        assert len(data) == 1
        assert data[0]['relationships']['content_object']['data'][
            'type'] == 'Ticket'

        resp = self.client.get(
            f'/api/users/{test_user.email}/purchased-items/?filter[item_type]=videocourse'
        )
        assert resp.status_code == 200
        data = resp.json()['data']
        assert len(data) == 1
        assert data[0]['relationships']['content_object']['data'][
            'type'] == 'VideoCourse'

        test_vl_oi1 = OrderItemVideoLectureFactory(customer=test_user,
                                                   is_paid=True)
        resp = self.client.get(
            f'/api/users/{test_user.email}/purchased-items/?filter[item_type]=videolecture&filter[lecturer.id]={test_vl.lecturer.id}'
        )
        assert resp.status_code == 200
        data = resp.json()['data']
        assert len(data) == 1
        assert data[0]['relationships']['content_object']['data']['lecturer'][
            'name'] == test_vl.lecturer.name

        test_vc_oi1 = OrderItemVideoCourseFactory(customer=test_user,
                                                  is_paid=True)

        resp = self.client.get(
            f'/api/users/{test_user.email}/purchased-items/?filter[item_type]=videocourse&filter[lecturer.id]={test_videocourse.lecturer.id}'
        )
        assert resp.status_code == 200
        data = resp.json()['data']
        assert len(data) == 1
        assert data[0]['relationships']['content_object']['data']['lecturer'][
            'id'] == f'{test_videocourse.lecturer.id}'

    def test_purchased_items_search(self):
        test_user = UserFactory()
        test_vl = VideoLectureFactory(name='bar', description='bar')
        test_vl_oi = OrderItemVideoLectureFactory(customer=test_user,
                                                  content_object=test_vl,
                                                  is_paid=True)
        offline_lecture = OfflineLectureFactory(description="Footest")
        test_ticket = TicketFactory(offline_lecture=offline_lecture)
        test_ticket_oi = OrderItemTicketFactory(customer=test_user,
                                                content_object=test_ticket,
                                                is_paid=True)
        self.client.force_authenticate(user=test_user)
        resp = self.client.get(
            f'/api/users/{test_user.email}/purchased-items/?filter[search]=foot'
        )
        assert resp.status_code == 200
        data = resp.json()['data']
        assert len(data) == 1
        assert data[0]['id'] == f'{test_ticket_oi.id}'
        resp = self.client.get(
            f'/api/users/{test_user.email}/purchased-items/?filter[search]=toof'
        )
        assert resp.status_code == 200
        data = resp.json()['data']
        assert len(data) == 0
