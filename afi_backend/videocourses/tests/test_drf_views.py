import pytest
from afi_backend.users.tests.factories import UserFactory
from rest_framework.test import APIClient, force_authenticate
from afi_backend.videocourses.tests.factories import VideoCourseFactory, CourseLectureFactory

pytestmark = pytest.mark.django_db


def test_videocourses_translated():
    test_user = UserFactory(email='test@test.ru', password='pass')
    test_name_ru = 'Тестовое Имя'
    test_name_en = 'Test Name'
    VideoCourseFactory(name_ru=test_name_ru, name_en=test_name_en)

    # # Locale set to en-US
    client = APIClient()
    client.force_authenticate(user=test_user)
    response = client.get('/api/videocourses/', None,
                          **{"HTTP_ACCEPT_LANGUAGE": "en-US"})
    assert response.data['results'][0]['name'] == test_name_en
    client.force_authenticate(user=None)

    # # Locale set to ru-RU
    client = APIClient()
    client.force_authenticate(user=test_user)
    response = client.get('/api/videocourses/',
                          **{"HTTP_ACCEPT_LANGUAGE": "ru-RU"})
    assert response.data['results'][0]['name'] == test_name_ru


def test_course_lectures_translated():
    test_user = UserFactory(email='test@test.ru', password='pass')
    test_name_ru = 'Тестовое Имя'
    test_name_en = 'Test Name'
    CourseLectureFactory(name_ru=test_name_ru, name_en=test_name_en)

    # # Locale set to en-US
    client = APIClient()
    client.force_authenticate(user=test_user)
    response = client.get('/api/videocourses/?include=lectures', None,
                          **{"HTTP_ACCEPT_LANGUAGE": "en-US"})
    assert response.json()['included'][0]['attributes']['name'] == test_name_en
    client.force_authenticate(user=None)

    # # Locale set to ru-RU
    client = APIClient()
    client.force_authenticate(user=test_user)
    response = client.get('/api/videocourses/?include=lectures',
                          **{"HTTP_ACCEPT_LANGUAGE": "ru-RU"})

    assert response.json()['included'][0]['attributes']['name'] == test_name_ru
