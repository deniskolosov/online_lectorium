from .api.views import PaymentCreateView
from django.urls import path


app_name = 'payments'
urlpatterns = [
    path("payment/", PaymentCreateView.as_view(), name="payment-create-view", ),
]
