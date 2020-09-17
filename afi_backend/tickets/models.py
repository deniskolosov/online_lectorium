import logging

from django.db import models

import uuid
from afi_backend.users.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from afi_backend.payments.models import Payable
from afi_backend.events.models import OfflineLecture

logger = logging.getLogger(__name__)


class Ticket(Payable):
    offline_lecture = models.ForeignKey(OfflineLecture,
                                        on_delete=models.CASCADE,
                                        null=True,
                                        blank=True,
                                        related_name='tickets')

    def generate_qr_code(self):
        logger.info("Generating qr code for {self}")
        return QRCode.objects.create(ticket=self, scanned=False)

    def do_afterpayment_logic(self):
        logger.info(f"Generating qr code for ticket{self}")
        self.generate_qr_code()

    def get_qr_code(self):
        return self.qrcode.code

    @property
    def scanned(self):
        if hasattr(self, 'qrcode'):
            return self.qrcode.scanned
        return False


class QRCode(models.Model):
    code = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            primary_key=True)
    scanned = models.BooleanField(default=False)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, blank=True)

    def is_valid(self):
        return not self.scanned

    def activate(self):
        self.scanned = True
        self.save()
