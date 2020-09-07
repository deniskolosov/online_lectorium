from django.db import models

from afi_backend.users.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Ticket(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()

    def generate_qr_code(self):
        return QRCode(ticket=self, scanned=False)


class Event(models.Model):
    description = models.TextField()


class QRCode(models.Model):
    scanned = models.BooleanField(default=False)
    ticket = models.OneToOneField(Ticket,
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  primary_key=True)
