from django.db import models
from afi_backend.videocourses.models import VideoCourse
from afi_backend.events.models import VideoLecture
from djmoney.models.fields import MoneyField


class VideoCoursePackage(models.Model):
    price = MoneyField(max_digits=10,
                       decimal_places=2,
                       null=True,
                       default=1,
                       default_currency='RUB')
    videocourses = models.ManyToManyField(VideoCourse)


class VideoLecturePackage(models.Model):
    price = MoneyField(max_digits=10,
                       decimal_places=2,
                       null=True,
                       default=1,
                       default_currency='RUB')
    videolectures = models.ManyToManyField(VideoLecture)
