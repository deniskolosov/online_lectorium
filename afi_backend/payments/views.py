from django.conf import settings
from django.views.generic.base import TemplateView


class CloudpaymentsPaymentView(TemplateView):
    template_name = 'payments/cloudpayments.html'


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_id'] = settings.CLOUDPAYMENTS_ACCOUNT_ID
        context['foo'] = 'bar'
        return context
