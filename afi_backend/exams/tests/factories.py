import factory
from afi_backend.exams.models import Exam, Question, TestAssignment, Answer
from afi_backend.users.tests.factories import UserFactory
from django.contrib.contenttypes.models import ContentType
from afi_backend.events.tests.factories import VideoLectureFactory
from afi_backend.videocourses.tests.factories import VideoCoursePartFactory


class TestAssignmentFactory(factory.django.DjangoModelFactory):
    object_id = factory.SelfAttribute('content_object.id')
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object))

    class Meta:
        exclude = ['content_object']
        abstract = True


class TestAssignmentVideoLectureFactory(factory.django.DjangoModelFactory):
    content_object = factory.SubFactory(VideoLectureFactory)

    class Meta:
        model = TestAssignment


class TestAssigmentVideoCoursePartFactory(factory.django.DjangoModelFactory):
    content_object = factory.SubFactory(VideoCoursePartFactory)

    class Meta:
        model = TestAssignment



class ExamFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    test_assignment = factory.SubFactory(TestAssigmentVideoCoursePartFactory)

    class Meta:
        model = Exam


class QuestionFactory(factory.django.DjangoModelFactory):
    text = factory.Faker("text")

    class Meta:
        model = Question


class AnswerFactory(factory.django.DjangoModelFactory):
    question = factory.SubFactory(QuestionFactory)

    class Meta:
        model = Answer
