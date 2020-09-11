from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from afi_backend.users.api.views import UserViewSet
from afi_backend.tickets.api.views import TicketViewSet
from afi_backend.events.api.views import EventViewSet, OfflineLectureViewset
from afi_backend.payments.api.views import PaymentMethodViewset, PaymentCreateView, YandexWebhook, CloudpaymentsWebhook
from django.urls import path


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("payment_methods", PaymentMethodViewset)
router.register("tickets", TicketViewSet, basename='tickets')
router.register("events", EventViewSet, basename='events')
router.register("offline-lectures", OfflineLectureViewset, basename='offline-lectures')

urlpatterns = [
    path("payments/", view=PaymentCreateView.as_view(), name="payment-create-view"),
    path("checkout-wh/", YandexWebhook.as_view(), name="yandex-checkout-webhook"),
    path("cloudpayments-wh/", CloudpaymentsWebhook.as_view(), name="cloudpayments-webhook"),
 ]

app_name = "api"
urlpatterns += router.urls
