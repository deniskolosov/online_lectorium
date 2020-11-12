from django.db import models

from afi_backend.events.models import Category, Lecturer
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from djmoney.models.fields import MoneyField
from afi_backend.payments.models import Subscriptable
from afi_backend.exams.models import TestAssignment


class VideoCourseType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class VideoCourse(Subscriptable):
    name = models.CharField(max_length=255)
    description = models.TextField()
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    release_date = models.DateTimeField(default=timezone.now)
    picture = models.ImageField(upload_to='videocourses_pictures/')
    price = MoneyField(max_digits=10,
                       decimal_places=2,
                       null=True,
                       default=1,
                       default_currency='RUB')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    course_type = models.ForeignKey(VideoCourseType,
                                    on_delete=models.CASCADE,
                                    null=True)

    order_items = GenericRelation('cart.OrderItem',
                                  object_id_field='object_id',
                                  content_type_field='content_type',
                                  related_query_name='video_course')

    @property
    def is_released(self):
        return self.release_date < timezone.now()

    class Meta:
        ordering = ['id']


class VideoCoursePart(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    course = models.ForeignKey(VideoCourse,
                               on_delete=models.CASCADE,
                               related_name='parts')
    tests = GenericRelation(TestAssignment,
                            object_id_field='object_id',
                            content_type_field='content_type',
                            related_query_name='videocourse_part')


class CourseLecture(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(VideoCourse,
                               on_delete=models.CASCADE,
                               related_name='lectures')
    part = models.ForeignKey(VideoCoursePart,
                             on_delete=models.CASCADE,
                             related_name='lectures',
                             null=True)
    lecturer = models.ForeignKey(Lecturer,
                                 blank=True,
                                 null=True,
                                 help_text="Set if different from course",
                                 on_delete=models.CASCADE)
    video_link = models.FileField(upload_to="videcourses_lectures/")

    def save(self, *args, **kwargs):
        if self.lecturer is None:
            self.lecturer = self.course.lecturer
        super().save(*args, **kwargs)
