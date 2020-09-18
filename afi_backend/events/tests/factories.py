import factory
import factory.fuzzy
from django.core.files.base import ContentFile

from afi_backend.events.models import (
    Category,
    Lecturer,
    LectureRating,
    OfflineLecture,
)
from afi_backend.users.tests.factories import UserFactory


class LecturerFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    bio = factory.Faker("text")

    class Meta:
        model = Lecturer


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyChoice(["Архитектура", "Искусство", "Психология", "Кино", "Аниме"])
    description = "Описание категории"
    color = factory.fuzzy.FuzzyChoice(["#ae78be", "#be78be", "#ad78be", "#ce78be", "#df78be"])

    class Meta:
        model = Category


class LectureRatingFactory(factory.django.DjangoModelFactory):
    rating = 10
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = LectureRating


class OfflineLectureFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Offline lecture {n}")
    lecturer = factory.SubFactory(LecturerFactory)
    category = factory.SubFactory(CategoryFactory)
    rating = factory.SubFactory(LectureRatingFactory)
    lecture_date = factory.Faker("date_time")
    picture = factory.Faker("image_url")

    class Meta:
        model = OfflineLecture
