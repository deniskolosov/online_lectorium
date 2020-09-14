import time

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from djmoney.models.fields import MoneyField

from afi_backend.tickets.models import Ticket


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


class LectureBase(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    lecture_summary_file = models.FileField(upload_to='lecture_summaries/',
                                            blank=True,
                                            null=True)
    tickets = GenericRelation(Ticket)
    price = MoneyField(max_digits=10,
                       decimal_places=2,
                       null=True,
                       default_currency='RUB')


class OfflineLecture(LectureBase):
    address = models.TextField()
    lecture_date = models.DateTimeField()

    def lecture_date_ts(self):
        # Return lecture date as timestamp.
        ts = int(time.mktime(self.lecture_date.timetuple()))
        return ts
