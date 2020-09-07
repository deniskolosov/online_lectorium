import logging

from afi_backend.payments.models import Payment
from config import celery_app
from .models import Ticket

logger = logging.getLogger(__name__)


class PaymentNotPaid(Exception):
    pass


@celery_app.task(autoretry_for=PaymentNotPaid,
                 retry_backoff=True,
                 retry_kwargs={'max_retries': 5})
def generate_qr_code_if_paid(payment_id):
    """
    Periodically check if Payment is paid, if so, generate QR code for the ticket.
    """
    try:
        payment = Payment.objects.select_related('content_object.').get(
            id=payment_id)
    except Payment.DoesNotExist:
        logger.info(f"Wrong payment_id passed {payment_id}")

    if payment.status == Payment.PENDING:
        logger.info(
            f"Will retry generating code later for payment {payment_id}")
        raise PaymentNotPaid
    if payment.status == Payment.PAID and isinstance(payment.content_object,
                                                     Ticket):
        payment.content_object.generate_qr_code()
        logger.info(f"QR code for ticket {ticket } generated")
