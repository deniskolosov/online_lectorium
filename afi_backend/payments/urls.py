from .api.views import PaymentCreateView, YandexWebhook
from .views import CloudpaymentsPaymentView
from django.urls import path


app_name = 'payments'

urlpatterns = [
    path('cloudpayments/<str:description>/<int:amount>/<str:currency>/', CloudpaymentsPaymentView.as_view(), name='cloudpayments-payment-form'),
]
