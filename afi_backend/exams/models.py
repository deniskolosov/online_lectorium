from django.db import models

from afi_backend.users.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Question(models.Model):
    text = models.TextField()


class Answer(models.Model):
    text = models.TextField()
    correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')


class TestAssignment(models.Model):
    questions = models.ManyToManyField(Question)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True)

    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')


class Progress(models.Model):
    answered = models.ManyToManyField(Answer)


class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_assignment = models.ForeignKey(TestAssignment, on_delete=models.CASCADE)
    result = models.SmallIntegerField(blank=True, null=True)
    progress = models.ForeignKey(Progress, on_delete=models.CASCADE, blank=True, null=True)
