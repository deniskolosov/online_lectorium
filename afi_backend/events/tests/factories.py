import factory

from afi_backend.events.models import (
    LectureCategory,
    Lecturer,
    LectureRating,
    OfflineLecture,
)
from afi_backend.users.tests.factories import UserFactory


class LecturerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lecturer


class LectureCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LectureCategory


class LectureRatingFactory(factory.django.DjangoModelFactory):
    rating = 10
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = LectureRating


class OfflineLectureFactory(factory.django.DjangoModelFactory):
    lecturer = factory.SubFactory(LecturerFactory)
    category = factory.SubFactory(LectureCategoryFactory)
    rating = factory.SubFactory(LectureRatingFactory)
    lecture_date = factory.Faker("date_time")

    class Meta:
        model = OfflineLecture
