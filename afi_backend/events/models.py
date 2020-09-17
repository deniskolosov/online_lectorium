import time

from colorfield.fields import ColorField
from django.db import models
from rest_framework.exceptions import ValidationError

from afi_backend.users.models import User
from django.contrib.contenttypes.fields import (GenericForeignKey,
    GenericRelation)
from django.contrib.contenttypes.models import ContentType
from djmoney.models.fields import MoneyField


class Event(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField()
    event_type = models.ForeignKey(ContentType,
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True)

    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('event_type', 'object_id')


class Lecturer(models.Model):
    name = models.CharField(max_length=256)
    userpic = models.ImageField(upload_to='lecturer_userpics/',
                                blank=True,
                                null=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class LectureCategory(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    color = ColorField(null=True)

    class Meta:
        verbose_name_plural = "Lecture categories"


class LectureRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()


class LectureBase(models.Model):
    name = models.CharField(max_length=256)
    picture = models.ImageField(upload_to='lecture_pictures', null=True, blank=True)
    description = models.TextField()
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    lecture_summary_file = models.FileField(upload_to='lecture_summaries/',
                                            blank=True,
                                            null=True)
    price = MoneyField(max_digits=10,
                       decimal_places=2,
                       null=True,
                       default_currency='RUB')
    category = models.ForeignKey(LectureCategory, on_delete=models.CASCADE, null=True)
    rating = models.ForeignKey(LectureRating, on_delete=models.CASCADE, null=True, blank=True)


class OfflineLecture(LectureBase):
    address = models.TextField()
    lecture_date = models.DateTimeField()
    capacity = models.PositiveSmallIntegerField(null=True)

    def lecture_date_ts(self):
        # Return lecture date as timestamp.
        ts = int(time.mktime(self.lecture_date.timetuple()))
        return ts

    @property
    def is_enough_space(self) -> bool:
        """
        Returns whether capacity allows to buy another ticket.
        """
        if self.capacity:
            # TODO :add filtering by paid tickets
            return self.tickets.count() < self.capacity
        raise ValidationError(f"Capacity is not set for Lecture {self}")

    def __str__(self):
        return f"Lecture {self.name}"
