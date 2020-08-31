from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from afi_backend.payments.urls import PaymentCreateView
from afi_backend.users.api.views import UserViewSet
from afi_backend.payments.api.views import PaymentMethodViewset
from django.urls import path


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("payment_methods", PaymentMethodViewset)

urlpatterns = [
    path("payments/", view=PaymentCreateView.as_view(), name="payment-create-view"),
 ]

app_name = "api"
urlpatterns += router.urls
