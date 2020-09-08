import uuid
from django.db import models
import logging

from afi_backend.users.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger(__name__)

class Ticket(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()

    def generate_qr_code(self):
        logger.info(f"Generating qr code for {self}")
        return QRCode.objects.create(ticket=self, scanned=False)

    def do_afterpayment_logic(self):
        logger.info(f"Generating qr code for ticket{self}")
        self.generate_qr_code()

    def get_qr_code(self):
        return self.qrcode.code

class QRCode(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    scanned = models.BooleanField(default=False)
    ticket = models.OneToOneField(Ticket,
                                  on_delete=models.CASCADE,
                                  blank=True)
    def is_valid(self):
        return not self.scanned

    def activate(self):
        self.scanned = True
        self.save()


class Event(models.Model):
    description = models.TextField()