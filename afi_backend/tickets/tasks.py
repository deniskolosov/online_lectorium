import logging

from afi_backend.payments.models import Payment
from config import celery_app
from .models import Ticket

logger = logging.getLogger(__name__)


class PaymentNotPaid(Exception):
    pass


@celery_app.task()
def call_do_afterpayment_logic(payment_id):
    """
    Call after payment logic related to Payment. Should be called after successful payment.
    """
    try:
        payment = Payment.objects.select_related('content_object.').get(
            id=payment_id)
    except Payment.DoesNotExist:
        logger.info(f"Wrong payment_id passed {payment_id}")

    payment.content_object.do_afterpayment_logic()
