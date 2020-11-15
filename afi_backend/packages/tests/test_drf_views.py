from afi_backend.packages.tests.factories import VideoCoursePackageFactory, VideoLecturePackageFactory
from rest_framework.test import APIClient, force_authenticate
from afi_backend.videocourses.tests.factories import VideoCourseFactory
from afi_backend.events.tests.factories import VideoLectureFactory
from afi_backend.users.tests.factories import UserFactory
import pytest

pytestmark = pytest.mark.django_db


def test_get_video_course_packages():
    test_videocourse_package = VideoCoursePackageFactory()
    test_videocourse_1 = VideoCourseFactory()
    test_videocourse_2 = VideoCourseFactory()
    test_videocourse_package.videocourses.add(test_videocourse_1,
                                              test_videocourse_2)
    test_videocourse_package.save()

    client = APIClient()
    test_user = UserFactory()

    client.force_authenticate(user=test_user)
    response = client.get(
        f'/api/packages/videocourses/{test_videocourse_package.id}/')
    assert response.status_code == 200
    assert response.json() == {
        'data': {
            'type': 'VideoCoursePackage',
            'id': str(test_videocourse_package.id),
            'attributes': {},
            'relationships': {
                'videocourses': {
                    'data': [{
                        'type': 'VideoCourse',
                        'id': str(test_videocourse_1.id)
                    }, {
                        'type': 'VideoCourse',
                        'id': str(test_videocourse_2.id)
                    }]
                }
            }
        }
    }


def test_get_video_lecture_packages():
    test_videolecture_package = VideoLecturePackageFactory()
    test_videolecture_1 = VideoLectureFactory()
    test_videolecture_2 = VideoLectureFactory()
    test_videolecture_package.videolectures.add(test_videolecture_1,
                                                test_videolecture_2)
    test_videolecture_package.save()

    client = APIClient()
    test_user = UserFactory()

    client.force_authenticate(user=test_user)
    response = client.get(
        f'/api/packages/videolectures/{test_videolecture_package.id}/')
    assert response.status_code == 200
    assert response.json() == {
        'data': {
            'type': 'VideoLecturePackage',
            'id': str(test_videolecture_package.id),
            'attributes': {},
            'relationships': {
                'videolectures': {
                    'data': [{
                        'type': 'VideoLecture',
                        'id': str(test_videolecture_1.id)
                    }, {
                        'type': 'VideoLecture',
                        'id': str(test_videolecture_2.id)
                    }]
                }
            }
        }
    }
