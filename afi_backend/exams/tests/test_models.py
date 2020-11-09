import pytest

from afi_backend.users.tests.factories import UserFactory
from afi_backend.exams.tests.factories import TestAssignmentVideoLectureFactory
from afi_backend.exams.models import Exam, Progress


pytestmark = pytest.mark.django_db

def test_progress_created_on_exam_creation():
    tu = UserFactory()
    ta = TestAssignmentVideoLectureFactory()
    exam = Exam.objects.create(user=tu, test_assignment=ta)
    assert exam.progress == Progress.objects.last()
