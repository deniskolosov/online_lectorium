from rest_framework.test import APIRequestFactory, force_authenticate

import pytest

from afi_backend.events.api.views import OfflineLectureViewset
from rest_framework.test import APIClient
from afi_backend.users.tests.factories import UserFactory
from afi_backend.events.tests.factories import OfflineLectureFactory


pytestmark = pytest.mark.django_db

def test_offline_lectures_translated():
    test_user = UserFactory()
    test_name_ru = 'Тестовое Имя'
    test_name_en = 'Test Name'
    OfflineLectureFactory(name_ru=test_name_ru, name_en=test_name_en)

    # Locale set to en-US
    client = APIClient()
    client.force_authenticate(user=test_user)
    response = client.get('/api/offline-lectures/', **{"HTTP_X_ACCEPT_LANGUAGE": "en-US"})
    assert response.data['results'][0]['name'] == test_name_en
    client.force_authenticate(user=None)

    # Locale set to ru-RU
    client = APIClient()
    client.force_authenticate(user=test_user)
    response = client.get('/api/offline-lectures/', **{"HTTP_X_ACCEPT_LANGUAGE": "ru-RU"})
    assert response.data['results'][0]['name'] == test_name_ru
