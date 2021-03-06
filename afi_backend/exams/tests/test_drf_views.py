import pytest

from afi_backend.events.tests.factories import VideoLectureFactory
from afi_backend.exams.tests.factories import MyTestAssignmentVideoLectureFactory, MyTestAssigmentVideoCoursePartFactory, ExamFactory, AnswerFactory
from afi_backend.users.tests.factories import UserFactory
from afi_backend.videocourses.tests.factories import VideoCoursePartFactory
from afi_backend.exams.models import Exam

from rest_framework.test import APIClient, force_authenticate

pytestmark = pytest.mark.django_db


class TestExamViewset:
    def test_create_exam_for_videolecture(self):
        test_video_lecture = VideoLectureFactory()
        test_assignment = MyTestAssignmentVideoLectureFactory(
            content_object=test_video_lecture)

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
        assert Exam.objects.last().test_assignment == test_assignment

    def test_create_exam_for_videocourse_part(self):
        test_videocourse_part = VideoCoursePartFactory()
        test_assignment = MyTestAssigmentVideoCoursePartFactory(
            content_object=test_videocourse_part)

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
        assert Exam.objects.last().test_assignment == test_assignment

    def test_get_progress(self):
        client = APIClient()
        test_user = UserFactory()
        test_assignment = MyTestAssignmentVideoLectureFactory()
        test_exam = ExamFactory(user=test_user,
                                test_assignment=test_assignment)
        test_answer = AnswerFactory(correct=True)
        test_exam.progress.chosen_answers.add(test_answer)
        test_exam.progress.save()

        client.force_authenticate(user=test_user)
        response = client.get(f'/api/exams/{test_exam.id}/progress/')
        assert response.json() == {
            'data': {
                'type': 'Progress',
                'id': str(test_exam.progress.id),
                'attributes': {},
                'relationships': {
                    'chosen_answers': {
                        'meta': {
                            'count': 1
                        },
                        'data': [{
                            'type': 'Answer',
                            'id': str(test_answer.id)
                        }]
                    }
                }
            }
        }

    def test_update_progress(self):
        client = APIClient()
        test_user = UserFactory()
        test_assignment = MyTestAssignmentVideoLectureFactory()
        test_answer = AnswerFactory(correct=True)
        test_exam = ExamFactory(user=test_user,
                                test_assignment=test_assignment)

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

        response = client.put(f'/api/exams/{test_exam.id}/progress/',
                              test_data)

        assert response.json() == {
            'data': {
                'type': 'Progress',
                'id': str(test_exam.progress.id),
                'attributes': {},
                'relationships': {
                    'chosen_answers': {
                        'meta': {
                            'count': 1
                        },
                        'data': [{
                            'type': 'Answer',
                            'id': str(test_answer.id)
                        }]
                    }
                }
            }
        }

    def test_get_results(self):
        client = APIClient()
        test_user = UserFactory()
        test_assignment = MyTestAssignmentVideoLectureFactory()
        test_correct_answer = AnswerFactory(correct=True)
        test_incorrect_answer = AnswerFactory(correct=False)
        test_exam = ExamFactory(user=test_user,
                                test_assignment=test_assignment)
        test_exam.progress.chosen_answers.add(test_correct_answer,
                                              test_incorrect_answer)
        test_exam.progress.save()

        client.force_authenticate(user=test_user)
        response = client.get(f'/api/exams/{test_exam.id}/')
        assert response.json() == {
            'data': {
                'id': test_exam.id,
                'test_assignment_id': test_assignment.id,
                'user': {
                    'type': 'User',
                    'id': str(test_user.id)
                },
                'results': {
                    'correct_answers': 1,
                    'total_answers': 2
                },
                'questions': []
            }
        }
