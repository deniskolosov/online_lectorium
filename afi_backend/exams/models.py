from django.db import models

from afi_backend.users.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from model_utils.models import post_save


class Question(models.Model):
    text = models.TextField()

    def __str__(self):
        return f"{self.text[:15]}"


class Answer(models.Model):
    text = models.TextField()
    correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')


class TestAssignment(models.Model):
    questions = models.ManyToManyField(Question)
    limit = models.Q(app_label='events', model='videolecture') | models.Q(app_label='videocourses', model='videocoursepart')
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     null=True,
                                     limit_choices_to=limit)

    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Test assignment for {self.content_object}"


# todo: create progress on exam creation
class Progress(models.Model):
    chosen_answers = models.ManyToManyField(Answer)


class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_assignment = models.ForeignKey(TestAssignment, on_delete=models.CASCADE)
    result = models.SmallIntegerField(blank=True, null=True)
    progress = models.OneToOneField(Progress, on_delete=models.CASCADE, blank=True, null=True, related_name='progress')


@receiver(post_save, sender=Exam)
def create_progress(sender, instance, created, **kwargs):
    if created:
        p = Progress.objects.create()
        instance.progress = p
        instance.save()
