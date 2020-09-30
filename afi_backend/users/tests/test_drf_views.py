import datetime
import io
from django.test import RequestFactory, modify_settings
from rest_framework.test import APIClient, force_authenticate
from typing import BinaryIO, Dict

import pytest
from PIL import Image

from afi_backend.users.api.views import UserViewSet
from afi_backend.users.models import User

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

        assert user in view.get_queryset()

    def test_me(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user
        test_bdate = datetime.date(2010, 10, 10)
        user.birthdate = test_bdate
        email = user.email

        view.request = request

        response = view.me(request)

        assert response.data == {
            "email": email,
            "url": f"http://testserver/api/users/{email}/",
            "birthdate": test_bdate.strftime("%Y-%m-%d"),
            "userpic": None,
            "name": user.name,
        }

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
        # TODO: test for uploading a userpic
        user_data = self._post_create_user()
        assert self.test_email == user_data['email']
        assert f'http://testserver/api/users/{self.test_email}/' == user_data[
            'url']
        user = User.objects.get(email=user_data['email'])
        assert user.email == self.test_email

    #     self.client.force_authenticate(user=user)
    #     pic = self._generate_photo_file()
    #     data = {'userpic': pic}
    #     from rest_framework.test import RequestsClient
    #     client = RequestsClient()
    #     resp = client.post('http://testserver/api/auth-token/', data={"email": "a@a.ru", "password": "123456"})

    #     # response = self.client.put('/api/users/{user.username}/upload-userpic/', data, format='multipart')
    #     assert False
