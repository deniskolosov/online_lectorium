import logging
import time

from colorfield.fields import ColorField
from django.db import models
from rest_framework.exceptions import ValidationError

from afi_backend.cart.models import OrderItem
from afi_backend.payments import models as payment_models
from afi_backend.users.models import User
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from djmoney.models.fields import MoneyField
from afi_backend.payments.models import Subscriptable
from afi_backend.exams.models import TestAssignment

logger = logging.getLogger(__name__)


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


class Category(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    color = ColorField(null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class LectureRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()


class LectureBase(models.Model):
    name = models.CharField(max_length=256)
    picture = models.ImageField(upload_to='lecture_pictures',
                                null=True,
                                blank=True)
    description = models.TextField()
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    lecture_summary_file = models.FileField(upload_to='lecture_summaries/',
                                            blank=True,
                                            null=True)
    price = MoneyField(max_digits=10,
                       decimal_places=2,
                       null=True,
                       default=1,
                       default_currency='RUB')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    rating = models.ForeignKey(LectureRating,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)

    class Meta:
        ordering = ['id']


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
            return self.tickets_sold < self.capacity
        raise ValidationError(f"Capacity is not set for Lecture {self}")

    @property
    def tickets_sold(self) -> int:
        """
        Get number of tickets sold for this lecture
        """
        return self.tickets.filter(is_paid=True).count()

    def __str__(self):
        return f"Lecture {self.name}"


class VideoLectureCertificate(models.Model):
    certificate_file = models.FileField(
        upload_to="video_lecture_certificates/")

    def __str__(self):
        return str(self.certificate_file)


class UsersVideoLectureCertificates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    certificate = models.ForeignKey(VideoLectureCertificate,
                                    on_delete=models.CASCADE)


class VideoLecture(LectureBase, Subscriptable):
    vimeo_video_id = models.CharField(max_length=256, null=True)
    certificate = models.ForeignKey(VideoLectureCertificate,
                                    on_delete=models.CASCADE)
    order_items = GenericRelation(OrderItem,
                                  object_id_field='object_id',
                                  content_type_field='content_type',
                                  related_query_name='video_lecture')
    tests = GenericRelation(TestAssignment,
                            object_id_field='object_id',
                            content_type_field='content_type',
                            related_query_name='video_lecture')

    def __str__(self):
        return f"{self.name}"

    def do_afterpayment_logic(self, customer=None):
        logger.info("Adding Video Lectures to user purchases.")
        payment_models.VideoLectureOrderItem.objects.create(customer=customer,
                                                            is_paid=True,
                                                            video_lecture=self)


class VideoLectureBulletPoint(models.Model):
    text = models.TextField()
    video_lecture = models.ForeignKey(VideoLecture,
                                      null=True,
                                      on_delete=models.SET_NULL,
                                      related_name='bullet_points')

    def __str__(self):
        return f"Bullet point {self.text[:10]}"
