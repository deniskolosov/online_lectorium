from django.db import models
from afi_backend.users.models import User


class Question(models.Model):
    text = models.TextField()


class Answer(models.Model):
    text = models.TextField()
    correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')


class TestAssignment(models.Model):
    questions = models.ManyToManyField(Question)


class Progress(models.Model):
    answered = models.ManyToManyField(Answer)


class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_assignment = models.ForeignKey(TestAssignment, on_delete=models.CASCADE)
    result = models.SmallIntegerField()
    progress = models.ForeignKey(Progress, on_delete=models.CASCADE)
