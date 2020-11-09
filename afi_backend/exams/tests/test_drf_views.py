import pytest

from afi_backend.events.tests.factories import VideoLectureFactory
from afi_backend.exams.tests.factories import TestAssignmentVideoLectureFactory, TestAssigmentVideoCoursePartFactory, ExamFactory, AnswerFactory
from afi_backend.users.tests.factories import UserFactory
from afi_backend.videocourses.tests.factories import VideoCoursePartFactory

from rest_framework.test import APIClient, force_authenticate

pytestmark = pytest.mark.django_db


class TestExamViewset:
    def test_create_exam_for_videolecture(self):
        test_video_lecture = VideoLectureFactory()
        test_assignment = TestAssignmentVideoLectureFactory(content_object=test_video_lecture)

        client = APIClient()
        test_user = UserFactory()
        client.force_authenticate(user=test_user)
        test_data = {
            "data": {
                "type": "Exam",
                "attributes": {
                    "test_assignment_id": test_assignment.id,
                }
            }
        }
        response = client.post('/api/exams/', data=test_data)
        assert response.status_code == 201
        assert response.json()['data']['attributes']['test_assignment_id'] == test_assignment.id
        assert response.json()['data']['relationships']['user']['data']['id'] == str(test_user.id)

    def test_create_exam_for_videocourse_part(self):
        test_videocourse_part = VideoCoursePartFactory()
        test_assignment = TestAssigmentVideoCoursePartFactory(content_object=test_videocourse_part)

        client = APIClient()
        test_user = UserFactory()
        client.force_authenticate(user=test_user)
        test_data = {
            "data": {
                "type": "Exam",
                "attributes": {
                    "test_assignment_id": test_assignment.id,
                }
            }
        }
        response = client.post('/api/exams/', data=test_data)
        assert response.status_code == 201
        assert response.json()['data']['attributes']['test_assignment_id'] == test_assignment.id
        assert response.json()['data']['relationships']['user']['data']['id'] == str(test_user.id)

    def test_get_progress(self):
        client = APIClient()
        test_user = UserFactory()
        test_assignment = TestAssignmentVideoLectureFactory()
        test_exam = ExamFactory(user=test_user, test_assignment=test_assignment)
        test_answer = AnswerFactory(correct=True)
        test_exam.progress.chosen_answers.add(test_answer)
        test_exam.progress.save()

        client.force_authenticate(user=test_user)
        response = client.get(f'/api/exams/{test_exam.id}/progress/')
        assert response.json() == {'data':
                                   {'type': 'Progress',
                                    'id': str(test_exam.progress.id),
                                    'attributes': {},
                                    'relationships':
                                    {'chosen_answers': {'data': [{'type': 'Answer', 'id': str(test_answer.id)}]}}}}

    def test_update_progress(self):
        client = APIClient()
        test_user = UserFactory()
        test_assignment = TestAssignmentVideoLectureFactory()
        test_answer = AnswerFactory(correct=True)
        test_exam = ExamFactory(user=test_user, test_assignment=test_assignment)

        client.force_authenticate(user=test_user)
        test_data = {
            "data": {
                "type": "Exam",
                'id': str(test_exam.id),
                "attributes": {
                    "answer_id": test_answer.id,
                }
            }
        }

        response = client.put(f'/api/exams/{test_exam.id}/progress/', test_data)

        assert response.json() == {'data':
                                   {'type': 'Progress',
                                    'id': str(test_exam.progress.id),
                                    'attributes': {},
                                    'relationships': {'chosen_answers':
                                                      {'data': [{'type': 'Answer', 'id': str(test_answer.id)}]}}}}
