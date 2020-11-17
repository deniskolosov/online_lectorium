import logging

from django.db import models

import uuid
from afi_backend.events.models import OfflineLecture
from afi_backend.payments.models import Payable, Payment
from afi_backend.users.models import User
from afi_backend.cart.models import OrderItem
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger(__name__)


class Ticket(Payable):
    offline_lecture = models.ForeignKey(OfflineLecture,
                                        on_delete=models.CASCADE,
                                        null=True,
                                        blank=True,
                                        related_name='tickets')
    order_items = GenericRelation(OrderItem,
                                  content_type_field='content_type',
                                  object_id_field='object_id',
                                  related_query_name='ticket')

    def __str__(self):
        return f"Ticket #{self.id} for offline_lecture #{self.offline_lecture.id}"

    def generate_qr_code(self):
        logger.info("Generating qr code for {self}")
        return QRCode.objects.create(ticket=self, scanned=False)

    def do_afterpayment_logic(self, customer=None):
        logger.info(f"Generating qr code for ticket{self}")
        self.is_paid = True
        self.generate_qr_code()
        self.customer = customer
        self.save()

    def get_qr_code(self):
        if self.order_items.filter(is_paid=True).exists():
            return self.qrcode.code
        return None

    @property
    def scanned(self):
        if hasattr(self, 'qrcode'):
            return self.qrcode.scanned
        return False

    @property
    def price(self):
        return self.offline_lecture.price


def create_qrcode(sender, **kwargs):
    ticket = kwargs["instance"]
    if kwargs["created"]:
        qrcode = QRCode.objects.create(ticket=ticket, scanned=False)


models.signals.post_save.connect(create_qrcode, sender=Ticket)


class QRCode(models.Model):
    code = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            primary_key=True)
    scanned = models.BooleanField(default=False)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"QRCode #{self.id} for ticket #{self.ticket.id}"

    def is_valid(self):
        return not self.scanned

    def activate(self):
        self.scanned = True
        self.save()
