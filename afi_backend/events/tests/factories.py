import factory
import factory.fuzzy
from django.core.files.base import ContentFile
from django.utils import timezone

from afi_backend.events.models import (
    Category,
    Lecturer,
    LectureRating,
    LectureBase,
    OfflineLecture,
    VideoLectureCertificate,
    VideoLecture,
    VideoLectureBulletPoint,
)
from afi_backend.users.tests.factories import UserFactory


class LecturerFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    bio = factory.Faker("text")

    class Meta:
        model = Lecturer


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyChoice(
        ["Архитектура", "Искусство", "Психология", "Кино", "Аниме"])
    description = "Описание категории"
    color = factory.fuzzy.FuzzyChoice(
        ["#ae78be", "#be78be", "#ad78be", "#ce78be", "#df78be"])

    class Meta:
        model = Category


class LectureRatingFactory(factory.django.DjangoModelFactory):
    rating = 10
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = LectureRating


class VideoLectureCertificateFactory(factory.django.DjangoModelFactory):
    certificate_file = factory.Faker("file_name", extension="pdf")

    class Meta:
        model = VideoLectureCertificate


class BaseLectureFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Base lecture {n}")
    lecturer = factory.SubFactory(LecturerFactory)
    category = factory.SubFactory(CategoryFactory)
    rating = factory.SubFactory(LectureRatingFactory)
    picture = 'lecture_pictures/1573646089377-9wpu20ce.jpeg'

    class Meta:
        model = LectureBase


class OfflineLectureFactory(BaseLectureFactory):
    name = factory.Sequence(lambda n: f"Offline lecture {n}")
    lecture_date = factory.Faker("date_time",
                                 tzinfo=timezone.get_current_timezone())
    price = 1000

    class Meta:
        model = OfflineLecture


class VideoLectureFactory(BaseLectureFactory):
    name = factory.Sequence(lambda n: f"Video lecture {n}")
    vimeo_video_id = "123456"
    certificate = factory.SubFactory(VideoLectureCertificateFactory)
    price = 800

    class Meta:
        model = VideoLecture


class VideoLectureBulletPointFactory(factory.django.DjangoModelFactory):
    video_lecture = factory.SubFactory(VideoLectureFactory)
    text = factory.Faker("sentence")

    class Meta:
        model = VideoLectureBulletPoint
