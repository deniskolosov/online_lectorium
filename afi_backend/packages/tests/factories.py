import factory
from afi_backend.packages.models import VideoCoursePackage, VideoLecturePackage


class VideoCoursePackageFactory(factory.django.DjangoModelFactory):
    price = 1000

    class Meta:
        model = VideoCoursePackage


class VideoLecturePackageFactory(factory.django.DjangoModelFactory):
    price = 1000

    class Meta:
        model = VideoLecturePackage
