from datetime import timedelta
from time import sleep
from decimal import Decimal
from django.conf import settings

from afi_backend.payments.adaptors import get_adaptor_from_payment_type
from afi_backend.payments.models import PaymentMethod, Subscription
from config import celery_app
from django.utils import timezone
from afi_backend.payments.adaptors.base import AdaptorException
from random import randrange


@celery_app.task(autoretry_for=(AdaptorException,),
                 exponential_backoff=5,
                 retry_kwargs={'max_retries': 3},
                 retry_jitter=False)
def charge_user_due(
        provider_id: int,
        external_id: str,
        amount: Decimal,
        currency: str,
        description: str,
        subscription_id: int
) -> None:
    # Sleep random time from 1 to 20 sec. Then do request to provider.
    # (not running all tasks in the same time).
    sleep(randrange(20))
    adaptor = get_adaptor_from_payment_type(payment_type=provider_id)
    success = adaptor.charge_recurrent(external_id=external_id,
                                       amount=amount,
                                       currency=currency,
                                       description=description,)
    if not success:
        Subscription.objects.filter(id=subscription_id).update(is_active=False, due=None)
        return None

    Subscription.objects.filter(id=subscription_id).update(is_active=True,
                                                           due=timezone.now() + timedelta(
                                                               days=settings.SUBSCRIPTION_LENGTH_DAYS))


@celery_app.task()
def charge_user_monthly():
    """
    Find all subscriptions that are due today. Try to charge the user. If payment is revoked, cancel subscriptions
    If other error, try again.
    """
    # For every method create their adaptor and call adaptor's charge recurrent method with
    # sub ids

    for method, _ in PaymentMethod.PAYMENT_TYPES:
        qs = Subscription.objects.filter(payment_method__payment_type=method,
                                         is_active=True,
                                         due__lt=timezone.now()).values('external_id',
                                                                        'user_membership__membership__price',
                                                                        'user_membership__membership__price_currency',
                                                                        'id')
        for val in qs:
            charge_user_due.delay(provider_id=method,
                                  external_id=val['external_id'],
                                  amount=val['user_membership__membership__price'],
                                  currency=val['user_membership__membership__price_currency'],
                                  description=f"Payment for subsription #{val['id']}",
                                  subscription_id=val['id'])


@celery_app.task()
def end_finished_trial_subscriptions():
    """
    Create task which runs every day and checks for Subscriptions which are active,
        and on trial. Check whether their trial has ended and set them to not active.
    """
    Subscription.objects.filter(
        is_active=True,
        is_trial=True,
        created_at__lt=timezone.now() - timedelta(days=7)).update(is_active=False,
                                                                  is_trial=False)
