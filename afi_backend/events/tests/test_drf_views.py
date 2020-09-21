import pytest
from rest_framework.test import APIClient, force_authenticate

from afi_backend.events.api.views import OfflineLectureViewset
from afi_backend.events.tests.factories import OfflineLectureFactory
from afi_backend.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_offline_lectures_translated():
    test_user = UserFactory(email='test@test.ru', password='pass')
    test_name_ru = 'Тестовое Имя'
    test_name_en = 'Test Name'
    OfflineLectureFactory(name_ru=test_name_ru, name_en=test_name_en)

    # # Locale set to en-US
    client = APIClient()
    client.force_authenticate(user=test_user)
    response = client.get('/api/offline-lectures/', None,
                          **{"HTTP_ACCEPT_LANGUAGE": "en-US"})
    assert response.data['results'][0]['name'] == test_name_en
    client.force_authenticate(user=None)

    # # Locale set to ru-RU
    client = APIClient()
    client.force_authenticate(user=test_user)
    response = client.get('/api/offline-lectures/',
                          **{"HTTP_ACCEPT_LANGUAGE": "ru-RU"})
    assert response.data['results'][0]['name'] == test_name_ru
