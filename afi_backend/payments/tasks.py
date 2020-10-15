from time import sleep

from afi_backend.payments.adaptors import get_adaptor_from_payment_type
from afi_backend.payments.models import PaymentMethod, Subscription
from config import celery_app
from django.utils import timezone


@celery_app.task()
def charge_user_monthly():
    """
    Find all subscriptions that are due today. Try to charge the user. If payment is revoked, cancel subscriptions
    If other error, try again"
    """
    # for every method create their adaptor and call adaptor's charge recurrent method with
    # sub ids

    for method, _ in PaymentMethod.PAYMENT_TYPES:
        qs = Subscription.objects.filter(payment_method__payment_type=method,
                                         is_active=True,
                                         due__lt=timezone.now()).values('external_id',
                                                                        'user_membership__membership__price')

@celery_app.task()
def charge_users_due(provider_id: int, subscription_data: list):
    adaptor = get_adaptor_from_payment_type(payment_type=provider_id)
    for item in subscription_data:
        adaptor.charge_recurrent(external_id=subscription_data['external_id'],
                                 amount=subscription_data['user_membership__membership__price'])
        sleep(1)
