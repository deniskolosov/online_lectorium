import factory
from django.utils import timezone
from afi_backend.videocourses.models import VideoCourse, CourseLecture, VideoCoursePart
from afi_backend.events.tests import factories as events_factories


class VideoCourseFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Videocourse {n}")
    description = factory.Faker("text")
    lecturer = factory.SubFactory(events_factories.LecturerFactory)
    price = 800
    release_date = factory.Faker("date_time",
                                 tzinfo=timezone.get_current_timezone())

    picture = 'videocourses_pictures/1573646089377-9wpu20ce.jpeg'
    category = factory.SubFactory(events_factories.CategoryFactory)

    class Meta:
        model = VideoCourse


class VideoCoursePartFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Videocourse part {n}")
    description = factory.Faker("text")
    course = factory.SubFactory(VideoCourseFactory)

    class Meta:
        model = VideoCoursePart


class CourseLectureFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Videocourse lecture {n}")
    description = factory.Faker("text")
    course = factory.SubFactory(VideoCourseFactory)
    part = factory.SubFactory(VideoCoursePartFactory)

    class Meta:
        model = CourseLecture
